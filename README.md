# LogLens

A small, dependency-free Python CLI for quickly summarizing application log files.

LogLens scans plain-text logs, counts common severity levels, surfaces repeated errors, finds the busiest hour in the file, and gives the log a simple health classification.

## Features

- Counts `ERROR`, `WARN`, `INFO`, and `DEBUG` entries
- Treats `CRITICAL` and `FATAL` as errors
- Groups repeated exception/error names
- Finds the most active hour when timestamps are available
- Configurable number of top errors with `--top`
- Handles invalid file paths cleanly
- Uses only the Python standard library

## Run it

Python 3.9+ recommended.

```bash
python3 loglens.py sample.log
```

Show more error groups:

```bash
python3 loglens.py sample.log --top 10
```

## Example output

```text
LOG LENS
────────────────────────────────────────
File:          sample.log
Lines scanned: 14

ERRORS         5
WARNINGS       3
INFO           5
DEBUG          1

Top errors
────────────────────────────────────────
   2  ConnectionTimeout
   2  AuthenticationFailed
   1  RateLimitExceeded

Most active hour: 09:00–10:00 (6 lines)
Health: WATCH
```

## Tests

```bash
python3 -m unittest -v
```

## Why this exists

Log files are often the first place to look when an API, integration, or service starts behaving unexpectedly. This project is a deliberately small utility for practicing practical parsing and troubleshooting workflows without adding external dependencies.

## Roadmap

- JSON log support
- Filter by severity
- Date/time range filters
- Export summary as JSON
- Response-code aggregation
- Optional ANSI colors

## License

MIT
