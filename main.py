#!/usr/bin/env python3
"""The Word You'd Delete From the Dictionary — u-puan-the-word-you-d-delete-from-the-dictionary-9e774bc2.

The entry is one word: defenestration. It is the only word in English
for throwing someone out of a window, and it sounds exactly like the
act it names — long, formal, and faintly ridiculous. Delete it and the
language loses its single word for a whole category of cartoon violence;
every defenestration becomes, forever, just "threw him out the window".

The program writes that one word, and nothing else, to
/output/entry.txt. The word is pinned below by its exact byte count and
SHA-256, and the program reads the file back and holds it to both, plus
the gate (UTF-8 text, 1 to 77 characters, not only white space), before
it reports success — so a changed, truncated or padded output can never
slip out as the entry. The output is byte-identical on every run.
"""

import hashlib
import os

WORD = "defenestration"
EXPECTED_SHA256 = "3e2847017717948152dd0b18359a4a1e6eea7c734142373afce3cdcfcdac12d9"
EXPECTED_BYTES = 14
MAX_CHARS = 77


def choose_output_dir():
    """The grader provides /output; a local trial falls back to ./output."""
    for candidate in ("/output", "output"):
        try:
            os.makedirs(candidate, exist_ok=True)
            probe = os.path.join(candidate, ".write-test")
            with open(probe, "w", encoding="utf-8") as fh:
                fh.write("ok")
            os.remove(probe)
            return candidate
        except OSError:
            continue
    raise SystemExit("no writable output directory for entry.txt")


def verify(path, data):
    """Read the written file back and hold it to the pinned bytes, hash,
    character count and exact text. Any mismatch aborts the run."""
    with open(path, "rb") as fh:
        back = fh.read()
    if back != data:
        raise SystemExit("read-back bytes differ from the pinned word")
    if len(back) != EXPECTED_BYTES:
        raise SystemExit(f"byte count {len(back)} != pinned {EXPECTED_BYTES}")
    digest = hashlib.sha256(back).hexdigest()
    if digest != EXPECTED_SHA256:
        raise SystemExit(f"sha256 {digest} != pinned {EXPECTED_SHA256}")
    text = back.decode("utf-8")
    if len(text) < 1 or len(text) > MAX_CHARS:
        raise SystemExit(f"character count {len(text)} outside 1..{MAX_CHARS}")
    if not text.strip():
        raise SystemExit("entry is only white space")
    if text != WORD:
        raise SystemExit("entry text differs from the pinned word")
    return True


def main():
    data = WORD.encode("utf-8")
    if len(data) != EXPECTED_BYTES:
        raise SystemExit("pinned word does not match pinned byte count")
    out_dir = choose_output_dir()
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "wb") as fh:
        fh.write(data)
    verified = verify(path, data)
    if not verified:
        raise SystemExit("read-back verification failed")
    print(f"wrote {path}: {WORD!r} ({EXPECTED_BYTES} bytes, sha256 {EXPECTED_SHA256[:12]}...)")


if __name__ == "__main__":
    main()
