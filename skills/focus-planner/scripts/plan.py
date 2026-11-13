"""Original, standard-library-only helper. No network, credentials, or writes."""

import argparse
import json
from datetime import datetime
from pathlib import Path


def plan(data, minutes=45):
    start, end = (
        datetime.fromisoformat(data[k]) for k in ("window_start", "window_end")
    )
    if (
        start.tzinfo is None
        or end.tzinfo is None
        or start >= end
        or not 15 <= minutes <= 180
    ):
        raise ValueError("Use an increasing timezone-aware window and 15-180 minutes")
    occupied = []
    for event in data.get("events", []):
        a, b = (
            datetime.fromisoformat(event["start"]),
            datetime.fromisoformat(event["end"]),
        )
        if a.tzinfo is None or b.tzinfo is None or b <= a:
            raise ValueError("Every event requires increasing timezone-aware times")
        if a < end and b > start:
            occupied.append((max(a, start), min(b, end)))
    cursor, gaps = start, []
    for a, b in sorted(occupied) + [(end, end)]:
        if (a - cursor).total_seconds() >= minutes * 60:
            gaps.append(
                {
                    "start": cursor.isoformat(),
                    "end": a.isoformat(),
                    "available_minutes": int((a - cursor).total_seconds() / 60),
                }
            )
        cursor = max(cursor, b)
    return {"requested_minutes": minutes, "suggestions": gaps}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path)
    parser.add_argument("--example", action="store_true")
    parser.add_argument("--minutes", type=int, default=45)
    args = parser.parse_args()
    if args.example:
        data = {
            "window_start": "2026-11-05T09:00:00-08:00",
            "window_end": "2026-11-05T17:00:00-08:00",
            "events": [
                {
                    "start": "2026-11-05T09:30:00-08:00",
                    "end": "2026-11-05T10:30:00-08:00",
                },
                {
                    "start": "2026-11-05T10:00:00-08:00",
                    "end": "2026-11-05T11:00:00-08:00",
                },
                {
                    "start": "2026-11-05T14:00:00-08:00",
                    "end": "2026-11-05T14:30:00-08:00",
                },
            ],
        }
    elif args.input:
        data = json.loads(args.input.read_text(encoding="utf-8"))
    else:
        parser.error("Choose --example or --input")
    print(json.dumps(plan(data, args.minutes), indent=2))
