"""Verify every exercise and write exercises.json.   Usage: python tools/build_exercises.py"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))

from harness import _pl_run  # noqa: E402
from exercises_src import EXERCISES  # noqa: E402
import exercises_more  # noqa: E402,F401  (adds to EXERCISES)

# Order of the sections in the app. Inside a section: easy first, then the order written.
TOPICS = ["Basics", "Strings", "Conditions", "Loops", "Lists", "Functions", "Dictionaries", "Tuples & sets",
          "Comprehensions", "Errors", "Classes", "Recursion", "Grids", "Logic puzzles", "Challenges"]
# Levels for the first batch, which was written before levels existed.
LEVELS = {"count-vowels": 2, "leap-year": 2, "fizzbuzz": 2, "second-largest": 2, "palindrome": 2, "fibonacci": 2,
          "word-count": 2, "most-expensive": 2, "long-words": 2, "to-int": 2, "bank-account": 2,
          "is-prime": 2, "anagrams": 2, "caesar": 3}
for e in EXERCISES:
    e["level"] = LEVELS.get(e["id"], e["level"])
unknown = {e["topic"] for e in EXERCISES} - set(TOPICS)
if unknown:
    sys.exit(f"Add these topics to TOPICS in build_exercises.py: {unknown}")
EXERCISES.sort(key=lambda e: (TOPICS.index(e["topic"]), e["level"]))

problems = []
seen = set()
for e in EXERCISES:
    if e["id"] in seen:
        problems.append(f"{e['id']}: duplicate id")
    seen.add(e["id"])
    solved = json.loads(_pl_run(e["solution"], e["tests"], e["stdin"]))
    if solved["passed"] is not True:
        problems.append(f"{e['id']}: reference solution fails -> {solved['error'] or solved['message']}")
    untouched = json.loads(_pl_run(e["starter"], e["tests"], e["stdin"]))
    if untouched["passed"] is True:
        problems.append(f"{e['id']}: the starter code already passes the checks")

if problems:
    print("\n".join(problems))
    sys.exit(1)

public = [{k: v for k, v in e.items() if k != "solution"} for e in EXERCISES]
(ROOT / "exercises.json").write_text(json.dumps(public, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"OK - {len(public)} exercises written to exercises.json")
