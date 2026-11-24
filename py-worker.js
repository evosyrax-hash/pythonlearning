// Runs Python (Pyodide) off the main thread so an endless loop can be killed.
import { loadPyodide } from "./vendor/pyodide/pyodide.mjs";

let run;
try {
  const pyodide = await loadPyodide({ indexURL: new URL("./vendor/pyodide/", import.meta.url).href });
  const harness = await (await fetch(new URL("./harness.py", import.meta.url))).text();
  pyodide.runPython(harness);
  run = pyodide.globals.get("_pl_run");
  postMessage({ type: "ready" });
} catch (err) {
  postMessage({ type: "fatal", message: String(err?.message || err) });
}

onmessage = (e) => {
  const { code, tests, stdin } = e.data;
  try {
    postMessage({ type: "result", result: JSON.parse(run(code, tests || "", stdin || "")) });
  } catch (err) {
    // e.g. RecursionError deep enough to escape the harness
    postMessage({ type: "result", result: { output: "", error: String(err?.message || err), passed: tests ? false : null, message: "" } });
  }
};
