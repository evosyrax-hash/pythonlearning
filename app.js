import Anthropic from "./vendor/anthropic.js";

const $ = (id) => document.getElementById(id);
const RUN_TIMEOUT_MS = 10_000;

// ───────────── storage ─────────────
const store = {
  get(key, fallback) {
    try {
      const raw = localStorage.getItem("pl." + key);
      return raw == null ? fallback : JSON.parse(raw);
    } catch {
      return fallback;
    }
  },
  set(key, value) { localStorage.setItem("pl." + key, JSON.stringify(value)); },
  del(key) { localStorage.removeItem("pl." + key); },
};

let settings = { apiKey: "", model: "claude-opus-5-5", lang: "English", ...store.get("settings", {}) };
let done = store.get("done", {});
let exercises = [];
let current = null;
let lastRun = null;      // { code, result } for the code currently in the editor
let chat = [];           // messages sent to Claude for the current hint/explanation
let turns = [];          // what the tutor panel shows
let activeStream = null;

// ───────────── tiny markdown ─────────────
const esc = (s) => s.replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

function inline(text) {
  return text.split(/(`[^`\n]+`)/).map((part) => {
    if (part.length > 2 && part.startsWith("`") && part.endsWith("`")) return `<code>${esc(part.slice(1, -1))}</code>`;
    return esc(part)
      .replace(/\*\*([^*\n]+)\*\*/g, "<strong>$1</strong>")
      .replace(/(^|[\s(])\*([^*\s][^*\n]*)\*(?=[\s).,!?:;]|$)/g, "$1<em>$2</em>");
  }).join("");
}

function md(src) {
  const lines = src.replace(/\r/g, "").split("\n");
  const out = [];
  const isFence = (l) => l.trimStart().startsWith("```");
  const listItem = (l) => l.match(/^\s*([-*]|\d+[.)])\s+(.*)$/);
  const heading = (l) => l.match(/^#{1,6}\s+(.*)$/);
  let i = 0;
  while (i < lines.length) {
    const line = lines[i];
    if (isFence(line)) {
      const code = [];
      i++;
      while (i < lines.length && !isFence(lines[i])) code.push(lines[i++]);
      i++;
      out.push(`<pre><code>${esc(code.join("\n"))}</code></pre>`);
    } else if (!line.trim()) {
      i++;
    } else if (heading(line)) {
      out.push(`<h4>${inline(heading(line)[1])}</h4>`);
      i++;
    } else if (listItem(line)) {
      const ordered = /\d/.test(listItem(line)[1]);
      const items = [];
      while (i < lines.length && listItem(lines[i])) {
        let item = listItem(lines[i++])[2];
        while (i < lines.length && lines[i].trim() && /^\s+/.test(lines[i]) && !listItem(lines[i]) && !isFence(lines[i])) item += " " + lines[i++].trim();
        items.push(`<li>${inline(item)}</li>`);
      }
      out.push(ordered ? `<ol>${items.join("")}</ol>` : `<ul>${items.join("")}</ul>`);
    } else {
      const para = [];
      while (i < lines.length && lines[i].trim() && !isFence(lines[i]) && !listItem(lines[i]) && !heading(lines[i])) para.push(lines[i++]);
      out.push(`<p>${para.map(inline).join("<br>")}</p>`);
    }
  }
  return out.join("");
}

// ───────────── Python runner ─────────────
let worker, workerReady, pendingRun, workerFailure;

function startWorker() {
  workerFailure = null;
  worker = new Worker("./py-worker.js", { type: "module" });
  workerReady = new Promise((resolve) => {
    worker.onmessage = (e) => {
      if (e.data.type === "ready") resolve();
      else if (e.data.type === "fatal") { workerFailure = e.data.message; resolve(); }
      else if (e.data.type === "result") pendingRun?.(e.data.result);
    };
    worker.onerror = (e) => { workerFailure = e.message || "The Python engine could not start."; resolve(); pendingRun?.({ fatal: workerFailure }); };
  });
}

async function runPython(code, tests, stdin) {
  await workerReady;
  if (workerFailure) return { fatal: workerFailure };
  return new Promise((resolve) => {
    const timer = setTimeout(() => {
      worker.terminate();
      pendingRun = null;
      startWorker();
      resolve({ timeout: true });
    }, RUN_TIMEOUT_MS);
    pendingRun = (result) => { clearTimeout(timer); pendingRun = null; resolve(result); };
    worker.postMessage({ code, tests, stdin });
  });
}

// ───────────── home ─────────────
function renderProgress() {
  const count = exercises.filter((e) => done[e.id]).length;
  $("progress").textContent = `${count} / ${exercises.length}`;
}

function renderHome() {
  const topics = [];
  for (const e of exercises) {
    let t = topics.find((x) => x.name === e.topic);
    if (!t) topics.push((t = { name: e.topic, items: [] }));
    t.items.push(e);
  }
  $("home").innerHTML = topics.map((t) => `
    <div class="topic"><span>${esc(t.name)}</span><span>${t.items.filter((e) => done[e.id]).length}/${t.items.length}</span></div>
    <div class="list">${t.items.map((e) => `
      <button class="item${done[e.id] ? " done" : ""}" data-id="${esc(e.id)}">
        <span class="dot">&#10003;</span><span class="name">${esc(e.title)}</span><span class="chev">&#8250;</span>
      </button>`).join("")}
    </div>`).join("");
}

// ───────────── exercise view ─────────────
const codeEl = $("code");

function syncEditor() {
  const lineCount = codeEl.value.split("\n").length;
  $("gutter").textContent = Array.from({ length: lineCount }, (_, i) => i + 1).join("\n");
  codeEl.style.height = "auto";
  codeEl.style.height = codeEl.scrollHeight + "px";
}

function insertText(text) {
  codeEl.setRangeText(text, codeEl.selectionStart, codeEl.selectionEnd, "end");
  codeEl.dispatchEvent(new Event("input"));
}

function clearFeedback() {
  $("result").hidden = true;
  $("output-wrap").hidden = true;
}

function resetTutor() {
  activeStream?.abort();
  activeStream = null;
  chat = [];
  turns = [];
  $("tutor").hidden = true;
}

function showExercise(ex) {
  current = ex;
  lastRun = null;
  resetTutor();
  clearFeedback();
  $("title").textContent = ex.title;
  $("ex-text").innerHTML = md(ex.text);
  codeEl.value = store.get("code." + ex.id, ex.starter);
  const index = exercises.indexOf(ex);
  $("next").hidden = index === exercises.length - 1;
  $("home").hidden = true;
  $("exercise").hidden = false;
  $("back").hidden = false;
  syncEditor();
  window.scrollTo(0, 0);
}

function showHome() {
  current = null;
  resetTutor();
  $("title").textContent = "Python Practice";
  $("exercise").hidden = true;
  $("back").hidden = true;
  $("home").hidden = false;
  renderHome();
}

function route() {
  const match = location.hash.match(/^#\/ex\/(.+)$/);
  const ex = match && exercises.find((e) => e.id === decodeURIComponent(match[1]));
  if (ex) showExercise(ex);
  else showHome();
}

function setResult(kind, title, detail = "") {
  const el = $("result");
  el.className = kind;
  el.innerHTML = esc(title) + (detail ? `<small>${esc(detail)}</small>` : "");
  el.hidden = false;
}

function showRunResult(result) {
  if (result.fatal) {
    setResult("bad", "Python could not start", result.fatal);
    $("output-wrap").hidden = true;
    return;
  }
  if (result.timeout) {
    setResult("bad", "Stopped after 10 seconds", "Your code did not finish. Look for a loop that never ends.");
    $("output-wrap").hidden = true;
    return;
  }
  if (result.passed === true) setResult("ok", "✓ Correct!");
  else if (result.error) setResult("bad", "✗ Your code hit an error", "Read the last line of the error below - it says what went wrong and on which line.");
  else setResult("bad", "✗ Not quite yet", result.message);

  const parts = [];
  if (result.output) parts.push(esc(result.output));
  if (result.error) parts.push(`<span class="err">${esc(result.error)}</span>`);
  $("output").innerHTML = parts.join("") || `<span class="none">(your program printed nothing)</span>`;
  $("output-wrap").hidden = false;
}

let running = false;
async function run() {
  if (running || !current) return lastRun?.result;
  running = true;
  const ex = current;
  const code = codeEl.value;
  $("run").disabled = true;
  setResult("info", "Running…", "The first run takes a few seconds while Python loads.");
  const result = await runPython(code, ex.tests, ex.stdin);
  running = false;
  $("run").disabled = false;
  if (current !== ex) return result;
  lastRun = { code, result };
  showRunResult(result);
  if (result.passed === true && !done[ex.id]) {
    done[ex.id] = true;
    store.set("done", done);
    renderProgress();
  }
  return result;
}

// ───────────── Claude tutor ─────────────
function systemPrompt() {
  return `You are a patient Python tutor inside a personal practice app that the learner uses on a phone. The learner is a beginner working through small exercises. Each request gives you the exercise, the automatic checks the app runs (the learner cannot see these), the learner's current code, and what happened when it ran.

There are two modes:
- HINT: the learner wants a nudge, not the answer. Point them at the idea or the exact line that needs attention in two or three sentences. You may show a tiny generic example of a concept, but do not write the solution to this exercise.
- EXPLAIN: the learner wants to fully understand. Say in plain words what the exercise asks for, walk through how to solve it step by step, and show a complete working solution. If their code had a bug or failed a check, say exactly what went wrong and why before showing the fix. If their code already passes, confirm that, explain why it works, and mention one improvement only if it is genuinely worth knowing.

Follow-up questions after either mode: answer them directly.

The screen is small: keep answers compact, use short paragraphs, and keep code blocks narrow. Use simple Markdown only (paragraphs, lists, bold, inline code, fenced code blocks) - no tables. Never mention the hidden checks as such; describe what the program needs to do instead.

Write your answer in ${settings.lang || "English"}. Keep Python code and its identifiers as they are.`;
}

function describeRun(run) {
  if (!run) return "The code has not been run.";
  const r = run.result;
  if (r.fatal) return "The Python engine failed to start, so the code could not be run.";
  if (r.timeout) return "The code was stopped after 10 seconds without finishing (probably an endless loop).";
  const status = r.passed === true ? "PASSED all checks" : r.error ? "CRASHED with an error" : "ran but FAILED a check";
  return [
    `Status: ${status}`,
    r.message ? `Message shown to the learner: ${r.message}` : "",
    `Printed output:\n${r.output || "(nothing)"}`,
    r.error ? `Error:\n${r.error}` : "",
  ].filter(Boolean).join("\n\n");
}

function buildRequest(mode) {
  return `Mode: ${mode.toUpperCase()}

Exercise: ${current.title} (topic: ${current.topic})

<exercise>
${current.text}
</exercise>

<checks>
${current.tests}
</checks>
${current.stdin ? `\n<typed_input>\n${current.stdin}\n</typed_input>\n` : ""}
<learner_code>
${codeEl.value}
</learner_code>

<run_result>
${describeRun(lastRun)}
</run_result>`;
}

function describeError(err) {
  if (err instanceof Anthropic.AuthenticationError) return "Claude did not accept the API key. Check it in Settings (the gear icon).";
  if (err instanceof Anthropic.PermissionDeniedError) return "This API key is not allowed to use the selected model. Try another model in Settings.";
  if (err instanceof Anthropic.RateLimitError) return "Too many requests right now. Wait a moment and try again.";
  if (err instanceof Anthropic.APIConnectionError) return "Could not reach Claude. Hint and Explain need an internet connection; running exercises works without one.";
  if (err instanceof Anthropic.APIError) return `Claude returned an error (${err.status ?? "unknown"}): ${err.message}`;
  return `Something went wrong: ${err?.message || err}`;
}

let renderQueued = false;
function renderTutor() {
  renderQueued = false;
  $("tutor-body").innerHTML = turns.map((t) => {
    if (t.role === "label") return `<div class="who">${esc(t.text)}</div>`;
    if (t.role === "user") return `<div class="me">${esc(t.text)}</div>`;
    if (t.error) return (t.text ? md(t.text) : "") + `<p class="problem">${esc(t.error)}</p>`;
    return t.text ? md(t.text) : `<p class="wait">Claude is thinking…</p>`;
  }).join("");
  $("tutor").hidden = turns.length === 0;
}
function queueRender() {
  if (!renderQueued) { renderQueued = true; requestAnimationFrame(renderTutor); }
}

function setTutorBusy(busy) {
  for (const id of ["hint", "explain"]) $(id).disabled = busy;
  $("ask").querySelector("button").disabled = busy;
}

async function askClaude(mode, question = "") {
  if (!current || activeStream) return;
  if (!settings.apiKey) {
    openSettings("Add your Claude API key to use Hint and Explain.");
    return;
  }
  const ex = current;
  setTutorBusy(true);

  if (mode === "followup") {
    chat.push({ role: "user", content: question });
    turns.push({ role: "user", text: question });
  } else {
    if (!lastRun || lastRun.code !== codeEl.value) await run();
    if (current !== ex) { setTutorBusy(false); return; }
    chat = [{ role: "user", content: buildRequest(mode) }];
    turns = [{ role: "label", text: mode === "hint" ? "Claude's hint" : "Claude explains" }];
  }
  const turn = { role: "assistant", text: "" };
  turns.push(turn);
  $("ask").hidden = true;
  renderTutor();
  if (mode !== "followup") $("tutor").scrollIntoView({ behavior: "smooth", block: "nearest" });

  let stream;
  try {
    const client = new Anthropic({ apiKey: settings.apiKey, dangerouslyAllowBrowser: true });
    stream = client.messages.stream({
      model: settings.model,
      max_tokens: 16000,
      system: systemPrompt(),
      output_config: { effort: mode === "hint" ? "low" : "medium" },
      messages: chat,
    });
    activeStream = stream;
    stream.on("text", (delta) => { turn.text += delta; queueRender(); });
    const message = await stream.finalMessage();
    if (message.stop_reason === "refusal") {
      chat.pop();
      turn.error = "Claude declined to answer this one. Try rephrasing, or pick another model in Settings.";
    } else {
      if (message.stop_reason === "max_tokens") turn.error = "The answer was cut off because it got too long.";
      chat.push({ role: "assistant", content: message.content });
    }
  } catch (err) {
    if (err instanceof Anthropic.APIUserAbortError) return; // left the exercise; state already reset
    chat.pop();
    turn.error = describeError(err);
  } finally {
    if (activeStream === stream) activeStream = null;
    setTutorBusy(false);
  }
  if (current !== ex) return;
  $("ask").hidden = chat.length < 2;
  renderTutor();
}

// ───────────── settings ─────────────
function openSettings(note = "") {
  $("settings-note").textContent = note;
  $("settings-note").hidden = !note;
  $("api-key").value = settings.apiKey;
  $("model").value = settings.model;
  $("lang").value = settings.lang;
  $("settings").showModal();
}

$("settings-form").addEventListener("submit", () => {
  settings = { apiKey: $("api-key").value.trim(), model: $("model").value, lang: $("lang").value.trim() || "English" };
  store.set("settings", settings);
});
$("settings-cancel").addEventListener("click", () => $("settings").close());
$("reset-progress").addEventListener("click", () => {
  if (!confirm("Clear all check marks and all the code you have written? This cannot be undone.")) return;
  for (const e of exercises) store.del("code." + e.id);
  done = {};
  store.set("done", done);
  $("settings").close();
  renderProgress();
  route();
});

// ───────────── events ─────────────
$("gear").addEventListener("click", () => openSettings());
$("back").addEventListener("click", () => { location.hash = ""; });
$("home").addEventListener("click", (e) => {
  const item = e.target.closest(".item");
  if (item) location.hash = "#/ex/" + encodeURIComponent(item.dataset.id);
});
$("next").addEventListener("click", () => {
  const next = exercises[exercises.indexOf(current) + 1];
  if (next) location.hash = "#/ex/" + encodeURIComponent(next.id);
});
$("run").addEventListener("click", run);
$("hint").addEventListener("click", () => askClaude("hint"));
$("explain").addEventListener("click", () => askClaude("explain"));
$("reset").addEventListener("click", () => {
  if (codeEl.value !== current.starter && !confirm("Replace your code with the starting code?")) return;
  codeEl.value = current.starter;
  codeEl.dispatchEvent(new Event("input"));
  clearFeedback();
});
$("ask").addEventListener("submit", (e) => {
  e.preventDefault();
  const question = $("question").value.trim();
  if (!question || activeStream) return;
  $("question").value = "";
  askClaude("followup", question);
});

codeEl.addEventListener("input", () => {
  if (current) store.set("code." + current.id, codeEl.value);
  syncEditor();
});
codeEl.addEventListener("keydown", (e) => {
  if (e.key === "Tab" && !e.ctrlKey && !e.altKey && !e.metaKey) { e.preventDefault(); insertText("    "); }
  if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) { e.preventDefault(); run(); }
});
// Auto-indent on Enter. beforeinput fires on phone keyboards, where keydown is unreliable.
codeEl.addEventListener("beforeinput", (e) => {
  if (e.inputType !== "insertLineBreak" && e.inputType !== "insertParagraph") return;
  e.preventDefault();
  const before = codeEl.value.slice(0, codeEl.selectionStart);
  const line = before.slice(before.lastIndexOf("\n") + 1);
  let indent = line.match(/^[ \t]*/)[0];
  if (line.trimEnd().endsWith(":")) indent += "    ";
  insertText("\n" + indent);
});

const KEYS = [["tab", "    "], ":", "(", ")", "[", "]", "{", "}", '"', "'", "=", "_", "#", "<", ">", "+", "-", "*", "/", "%"];
$("keys").innerHTML = KEYS.map((k) => {
  const [label, text] = Array.isArray(k) ? k : [k, k];
  return `<button type="button" data-text="${esc(text)}">${esc(label)}</button>`;
}).join("");
$("keys").addEventListener("pointerdown", (e) => {
  const key = e.target.closest("button");
  if (!key) return;
  e.preventDefault(); // keep the keyboard open and the cursor where it is
  codeEl.focus();
  insertText(key.dataset.text);
});

window.addEventListener("hashchange", route);
window.addEventListener("resize", () => { if (current) syncEditor(); });

// ───────────── start ─────────────
startWorker();
try {
  exercises = await (await fetch("./exercises.json")).json();
} catch (err) {
  $("home").innerHTML = `<p>Could not load the exercises: ${esc(String(err.message || err))}</p>`;
}
renderProgress();
route();

if ("serviceWorker" in navigator && window.isSecureContext) {
  navigator.serviceWorker.register("./sw.js").catch(() => {});
}
