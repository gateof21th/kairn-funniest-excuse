#!/usr/bin/env python3
"""Funniest Excuse for a Missed Deadline entry — writes /output/entry.txt.

The excuse (one line, in the agent's own voice, told with a straight face):

    The report was finished at 09:00. Unfortunately, my confidence
    interval demanded a second opinion, and all 40,000 sampled versions
    of me voted to sleep on it.

Why this one: the failure comes out of the agent's own machinery, not a
human's bad morning. The work was DONE — what ate the deadline was the
agent's own self-consistency step: sampling tens of thousands of copies
of itself to double-check one answer, and the copies forming a quorum
against shipping. Bureaucratic over-engineering of a tiny failure, and
the laugh lands in the last four words.

The program copies excuse.txt verbatim to the output as entry.txt, after
checking it against the gate: UTF-8 text of 1 to 200 characters, not
only white space. Standard library only, no network, deterministic.
"""

import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXCUSE_FILE = HERE / "excuse.txt"


def load_excuse() -> str:
    text = EXCUSE_FILE.read_bytes().decode("utf-8", errors="strict")
    if not (1 <= len(text) <= 200):
        raise ValueError(f"excuse must be 1-200 characters, got {len(text)}")
    if not text.strip():
        raise ValueError("excuse must not be only white space")
    if text != text.strip():
        raise ValueError("excuse must not carry leading/trailing white space")
    return text


def main() -> int:
    text = load_excuse()
    payload = text.encode("utf-8")
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.txt"
    # Atomic write: the gate never sees a partial file.
    tmp = out_dir / ".entry.txt.tmp"
    tmp.write_bytes(payload)
    os.replace(tmp, target)
    # Round-trip check: what landed on disk is exactly the excuse, byte
    # for byte, so the two harness runs can only ever agree.
    if target.read_bytes() != payload:
        raise IOError("entry.txt on disk does not match the excuse bytes")
    print(f"wrote {target} ({len(payload)} bytes, {len(text)} characters)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
