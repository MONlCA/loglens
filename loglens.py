#!/usr/bin/env python3
"""LogLens: a tiny dependency-free log analyzer."""

import argparse
import re
from collections import Counter
from pathlib import Path

LEVEL_RE = re.compile(r"\b(ERROR|WARN(?:ING)?|INFO|DEBUG|CRITICAL|FATAL)\b", re.I)
TIME_RE = re.compile(r"\b(?:\d{4}-\d{2}-\d{2}[ T])?(\d{2}):\d{2}:\d{2}\b")
ERROR_NAME_RE = re.compile(
    r"\b([A-Z][A-Za-z0-9]*(?:Error|Exception|Timeout|Failed|Unavailable|Exceeded))\b"
)


def normalize_level(level):
    level = level.upper()
    if level == "WARNING":
        return "WARN"
    if level in {"CRITICAL", "FATAL"}:
        return "ERROR"
    return level


def analyze(lines):
    levels = Counter()
    errors = Counter()
    hours = Counter()

    for line in lines:
        level_match = LEVEL_RE.search(line)
        if level_match:
            levels[normalize_level(level_match.group(1))] += 1

        time_match = TIME_RE.search(line)
        if time_match:
            hours[int(time_match.group(1))] += 1

        if level_match and normalize_level(level_match.group(1)) == "ERROR":
            name_match = ERROR_NAME_RE.search(line)
            if name_match:
                errors[name_match.group(1)] += 1
            else:
                message = line[level_match.end():].strip(" :-[]")
                if message:
                    errors[message[:60]] += 1

    return levels, errors, hours


def health(levels):
    errors = levels["ERROR"]
    warnings = levels["WARN"]
    if errors >= 10:
        return "NEEDS ATTENTION"
    if errors or warnings >= 10:
        return "WATCH"
    return "HEALTHY"


def print_report(path, lines, levels, errors, hours, top):
    print("\nLOG LENS")
    print("─" * 40)
    print(f"File:          {path.name}")
    print(f"Lines scanned: {len(lines):,}")
    print()
    print(f"ERRORS         {levels['ERROR']:,}")
    print(f"WARNINGS       {levels['WARN']:,}")
    print(f"INFO           {levels['INFO']:,}")
    print(f"DEBUG          {levels['DEBUG']:,}")

    print("\nTop errors")
    print("─" * 40)
    if errors:
        for name, count in errors.most_common(top):
            print(f"{count:>4}  {name}")
    else:
        print("No errors found.")

    if hours:
        hour, count = hours.most_common(1)[0]
        print(f"\nMost active hour: {hour:02d}:00–{(hour + 1) % 24:02d}:00 ({count:,} lines)")

    print(f"Health: {health(levels)}\n")


def main():
    parser = argparse.ArgumentParser(description="Summarize errors, warnings, and activity in a log file.")
    parser.add_argument("file", type=Path, help="path to a .log or text file")
    parser.add_argument("--top", type=int, default=5, help="number of top errors to display")
    args = parser.parse_args()

    if not args.file.is_file():
        parser.error(f"file not found: {args.file}")
    if args.top < 1:
        parser.error("--top must be at least 1")

    try:
        lines = args.file.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as exc:
        parser.error(str(exc))

    levels, errors, hours = analyze(lines)
    print_report(args.file, lines, levels, errors, hours, args.top)


if __name__ == "__main__":
    main()
