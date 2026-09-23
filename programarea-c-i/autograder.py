#!/usr/bin/env python3
"""Lab 1 default grader: build, public tests, and sanitizer."""
from __future__ import annotations

import datetime
import json
import os
import pathlib
import subprocess

classroom = os.environ.get("CLASSROOM", "")
assignment = os.environ.get("ASSIGNMENT", "")
assignment_type = os.environ.get("ASSIGNMENT_TYPE", "individual")
username = os.environ.get("USERNAME", "")
owner = os.environ.get("OWNER", "") or username
submission = os.environ.get("SUBMISSION_TAG", "")
commit_url = os.environ.get("COMMIT_URL", "")
release_url = os.environ.get("RELEASE_URL", "")
review_url = os.environ.get("REVIEW_URL", "") or commit_url

checks = [
    ("builds without warnings", ["make"]),
    ("public tests pass", ["make", "test"]),
    ("sanitizer tests pass", ["make", "sanitize"]),
]
results = []
for name, command in checks:
    proc = subprocess.run(command, cwd=os.getcwd(), capture_output=True, text=True, timeout=120, check=False)
    passed = proc.returncode == 0
    output = (proc.stdout + proc.stderr).strip()
    results.append({
        "test-name": name,
        "passed": passed,
        "score": 1 if passed else 0,
        "max-score": 1,
        "details": output[-4000:],
    })
    if not passed:
        break

result = {
    "schema": "classroom50/result/v1",
    "classroom": classroom,
    "assignment": assignment,
    "assignment_type": assignment_type,
    "owner": owner,
    "submission": submission,
    "commit": commit_url,
    "release": release_url,
    "review": review_url,
    "datetime": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "score": sum(item["score"] for item in results),
    "max-score": sum(item["max-score"] for item in results),
    "tests": results,
}
pathlib.Path("result.json").write_text(json.dumps(result, indent=2) + "\n")
print(f"autograder: {result['score']}/{result['max-score']}")
