#!/usr/bin/env python3
"""Readable Markdown from a Claude Code session transcript (.jsonl), for handoffs.

Keeps: user messages, assistant replies, tool calls (name + input, trimmed) and
tool results (trimmed). Drops: images (replaced by a marker), internal
reasoning blocks, app bookkeeping lines. Scrubs strings that look like API keys
or tokens before anything is written.

Usage: transcript_to_md.py SESSION.jsonl OUT.md [--title TITLE] [--max-input 3000] [--max-result 1500]
"""
from __future__ import annotations

import argparse
import json
import re

SECRET_RES = [
    re.compile(r"AIza[0-9A-Za-z_\-]{35}"),                 # Google API keys
    re.compile(r"\bgh[pousr]_[0-9A-Za-z]{30,}"),            # GitHub tokens
    re.compile(r"\bsk-(?:ant-)?[0-9A-Za-z_\-]{20,}"),       # Anthropic/OpenAI style keys
    re.compile(r"(?i)\bbearer\s+[0-9A-Za-z._\-]{20,}"),
    re.compile(r"\bya29\.[0-9A-Za-z._\-]{20,}"),            # Google OAuth access tokens
    re.compile(r"(?i)(password|passwd|secret|api[_-]?key)\s*[=:]\s*\S+"),
]


def scrub(s: str) -> str:
    for r in SECRET_RES:
        s = r.sub("[REDACTED]", s)
    return s


def trim(s: str, n: int) -> str:
    s = s if isinstance(s, str) else json.dumps(s, ensure_ascii=False)
    return s if len(s) <= n else s[:n] + f"\n… [{len(s) - n} more characters trimmed]"


def result_text(c) -> str:
    if isinstance(c, str):
        return c
    out = []
    for b in c or []:
        if isinstance(b, dict):
            if b.get("type") == "text":
                out.append(b.get("text", ""))
            elif b.get("type") == "image":
                out.append("[image]")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("out")
    ap.add_argument("--title", default="Session transcript")
    ap.add_argument("--max-input", type=int, default=3000)
    ap.add_argument("--max-result", type=int, default=1500)
    a = ap.parse_args()
    lines, first, last = [], None, None
    for raw in open(a.src, encoding="utf-8"):
        try:
            d = json.loads(raw)
        except json.JSONDecodeError:
            continue
        typ = d.get("type")
        if typ not in ("user", "assistant"):
            continue
        ts = (d.get("timestamp") or "")[:19].replace("T", " ")
        first = first or ts
        last = ts or last
        msg = d.get("message") or {}
        content = msg.get("content")
        if typ == "user":
            if isinstance(content, str):
                lines.append(f"\n### User — {ts}\n\n{content.strip()}\n")
                continue
            for b in content or []:
                if not isinstance(b, dict):
                    continue
                if b.get("type") == "text":
                    lines.append(f"\n### User — {ts}\n\n{b.get('text', '').strip()}\n")
                elif b.get("type") == "image":
                    lines.append(f"\n### User — {ts}\n\n[image attached]\n")
                elif b.get("type") == "tool_result":
                    txt = trim(result_text(b.get("content")), a.max_result)
                    lines.append(f"\n<details><summary>result</summary>\n\n```\n{txt}\n```\n</details>\n")
        else:
            for b in content if isinstance(content, list) else []:
                if not isinstance(b, dict):
                    continue
                if b.get("type") == "text" and b.get("text", "").strip():
                    lines.append(f"\n### Assistant — {ts}\n\n{b['text'].strip()}\n")
                elif b.get("type") == "tool_use":
                    inp = b.get("input") or {}
                    desc = inp.get("description") or ""
                    body = inp.get("command") or inp.get("prompt") or inp
                    lines.append(f"\n**Tool `{b.get('name')}`**{(' — ' + desc) if desc else ''}\n\n```\n{trim(body, a.max_input)}\n```\n")
    head = f"# {a.title}\n\nSource: `{a.src.split('/')[-1]}` · {first} → {last} (UTC) · images and internal reasoning omitted, long outputs trimmed, key-like strings redacted.\n"
    with open(a.out, "w", encoding="utf-8") as f:
        f.write(scrub(head + "".join(lines)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
