#!/usr/bin/env python3
"""Adds a stub entry for today's date to README.md if one doesn't already exist."""
import datetime
import re
import sys

README = "README.md"
today = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")

with open(README, "r", encoding="utf-8") as f:
    content = f.read()

if f"### {today}" in content:
    print(f"Entry for {today} already exists. Skipping.")
    sys.exit(0)

# --- Insert a new row into the index table (right after the header separator) ---
index_row = f"| {today} | [Untitled]() | TBD |\n"
table_header_pattern = r"(\| Date \| Topic \| Category \|\n\|[-\s|]+\|\n)"
match = re.search(table_header_pattern, content)
if match:
    insert_at = match.end()
    content = content[:insert_at] + index_row + content[insert_at:]

# --- Remove the placeholder example row if it's still the only one left ---
content = content.replace("| YYYY-MM-DD | [Entry title](#) | ML / DSA / GenAI / Frontend |\n", "", 1)

# --- Insert a new stub entry right after "## Entries" (newest on top) ---
stub_entry = f"""
### {today} — Untitled

**Category:** TBD

_Stub auto-created — fill this in with what you actually learned today._

```
# code snippet if relevant
```

**Why it matters / where I'll use it:**


---
"""

entries_marker = "## Entries\n"
idx = content.find(entries_marker)
if idx != -1:
    insert_at = idx + len(entries_marker)
    content = content[:insert_at] + stub_entry + content[insert_at:]
else:
    content += stub_entry

with open(README, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Added stub entry for {today}")
