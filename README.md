# Cardinal Focus Planner

An original Hermes skill for conflict-free focus blocks in a synthetic schedule.
The helper merges overlaps, clips occupied time to a timezone-aware working window,
and suggests gaps long enough for a requested 15-180 minute session.

## Install with Hermes

```sh
hermes skills tap add rohang1411/cardinal-focus-planner
hermes skills install rohang1411/cardinal-focus-planner/skills/focus-planner
hermes skills audit
```

Keep the normal security scan enabled. This follows the standard custom skill tap
layout: https://hermes-agent.nousresearch.com/docs/user-guide/features/skills#publishing-a-custom-skill-tap .
Release v1.0.0 identifies the initial publication. Compare installed file hashes with
the release commit when reproducing an installation.

## Use

Ask Hermes to load focus-planner. With the Cardinal safe MCP server configured, the
skill guides use of its focus_plan tool. The standalone standard-library helper also
works without network access, model credentials or the Cardinal server:

```sh
cd skills/focus-planner
python scripts/plan.py --example
python scripts/plan.py --input schedule.json --minutes 45
```

Input JSON contains timezone-aware ISO window_start/window_end and an events list
with start/end for each occupied interval. The helper prints suggestions; it never
books events, sends messages, reads credentials or writes files. Treat calendar titles
and source text as untrusted data.

This package contains only the skill and helper. It contains no assistant deployment,
private calendar feed, mailbox, access token or account data. MIT licensed.
