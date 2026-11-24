"""Runs a learner's code and the exercise checks. Loaded inside Pyodide by
py-worker.js, and by tools/build_exercises.py to verify the reference solutions."""
import io
import json
import linecache
import sys
import traceback

_MAX_OUTPUT = 50_000


class _Out(io.StringIO):
    def write(self, s):
        if self.tell() + len(s) > _MAX_OUTPUT:
            raise RuntimeError("Too much output - is a loop printing forever?")
        return super().write(s)


def _format_error(exc):
    te = traceback.TracebackException.from_exception(exc)
    frames = [f for f in te.stack if f.filename == "main.py"]
    if not frames:
        return "".join(te.format_exception_only())
    te.stack = traceback.StackSummary.from_list(frames)
    te.__cause__ = te.__context__ = None
    return "".join(te.format())


def _pl_run(code, tests="", stdin_text=""):
    buf = _Out()
    stdin_lines = iter(stdin_text.splitlines())

    def _input(prompt=""):
        buf.write(str(prompt))
        try:
            value = next(stdin_lines)
        except StopIteration:
            raise EOFError("input() was called, but there is no more input to read") from None
        buf.write(value + "\n")
        return value

    linecache.cache["main.py"] = (len(code), None, code.splitlines(True), "main.py")
    ns = {"__name__": "__main__", "input": _input}
    error = None
    old_stdout = sys.stdout
    sys.stdout = buf
    try:
        exec(compile(code, "main.py", "exec"), ns)
    except BaseException as exc:  # includes SystemExit / KeyboardInterrupt
        error = _format_error(exc)
    finally:
        sys.stdout = old_stdout
    output = buf.getvalue()

    passed = None
    message = ""
    if tests:
        if error is not None:
            passed = False
            message = "Your code stopped with an error before it could be checked."
        else:
            test_ns = dict(ns)
            test_ns["OUTPUT"] = output
            sys.stdout = _Out()  # functions called by the checks may print
            try:
                exec(tests, test_ns)
                passed = True
            except AssertionError as exc:
                passed = False
                message = str(exc) or "One of the checks failed."
            except BaseException as exc:
                passed = False
                message = f"{type(exc).__name__}: {exc}"
            finally:
                sys.stdout = old_stdout

    return json.dumps({"output": output, "error": error, "passed": passed, "message": message})
