"""Check a workflow evidence record without executing commands from the record."""

import argparse
import json
from pathlib import Path
import sys


def has_text(mapping, key):
    value = mapping.get(key)
    return isinstance(value, str) and bool(value.strip())


def validate(record, require_pass=False):
    if not isinstance(record, dict):
        return ["record must be an object"]
    errors = []
    if not has_text(record, "revision"):
        errors.append("revision must name the checked version or workspace")
    checks = record.get("checks")
    if not isinstance(checks, list) or not checks:
        return errors + ["checks must be a non-empty list"]
    criteria = set()
    for number, check in enumerate(checks, start=1):
        label = f"check {number}"
        if not isinstance(check, dict):
            errors.append(f"{label}: must be an object")
            continue
        for field in ("criterion", "entry", "expected"):
            if not has_text(check, field):
                errors.append(f"{label}: {field} is required")
        if has_text(check, "criterion"):
            criterion = check["criterion"].strip()
            if criterion in criteria:
                errors.append(f"{label}: duplicate criterion")
            criteria.add(criterion)
        status = check.get("status")
        if status in ("pass", "fail"):
            for field in ("observed", "evidence"):
                if not has_text(check, field):
                    errors.append(f"{label}: {field} is required for {status}")
        elif status == "unverified":
            if not has_text(check, "reason"):
                errors.append(f"{label}: reason is required for unverified checks")
        else:
            errors.append(f"{label}: status must be pass, fail, or unverified")
        if require_pass and status != "pass":
            errors.append(f"{label}: has not passed")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record", type=Path)
    parser.add_argument("--require-pass", action="store_true")
    arguments = parser.parse_args()
    try:
        record = json.loads(arguments.record.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        parser.exit(2, f"Cannot read evidence: {error}\n")
    errors = validate(record, arguments.require_pass)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"Valid evidence record with {len(record['checks'])} check(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
