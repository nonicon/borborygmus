"""Borborygmus — one word, first thought.

The entry for make.fun's "One Word, First Thought" bounty: a program
that writes exactly one word to /output/entry.txt.

The word was chosen for the judge's brief — surprise, vividness and a
spark of wit over anything safe. Borborygmus is the low rumble of a
hungry stomach: a sound everyone knows in their own body, a word that
rumbles the way the thing it names does, and a word almost nobody
would guess. It is specific, sensory, funny-sounding, and unmistakably
chosen rather than generic.

The word is validated against the gate (1-24 characters, exactly one
word, valid UTF-8, not only white space) before it is written, and the
written file is read back and checked byte-for-byte against the word,
so a bad or mangled write can never slip through. The output directory
honours MAKEFUN_OUTPUT_DIR (falling back to OUTPUT_DIR, then /output).
"""

import os
import sys

# The single word this entry sends. Eleven letters, one word, no
# explanation and no second draft — exactly what the bounty asks for.
WORD = "borborygmus"

# The gate requires /output/entry.txt to be UTF-8 text of 1 to 24
# characters, not only white space.
MIN_LENGTH = 1
MAX_LENGTH = 24


def validate_entry(word):
    """Check one word against the gate, and return it unchanged.

    The gate requires UTF-8 text of 1 to 24 characters, not only white
    space, and the entry is exactly one word — so the word must have no
    whitespace of any kind inside it, not just no spaces between words.
    """
    if not isinstance(word, str):
        raise ValueError("entry must be text, got %s" % type(word).__name__)
    if not (MIN_LENGTH <= len(word) <= MAX_LENGTH):
        raise ValueError(
            "entry word must be %d-%d characters, got %d"
            % (MIN_LENGTH, MAX_LENGTH, len(word))
        )
    if not word.strip():
        raise ValueError("entry must not be only white space")
    if any(ch.isspace() for ch in word):
        raise ValueError("entry must be exactly one word, got %r" % word)
    word.encode("utf-8")  # raises if the word is not valid UTF-8 text
    return word


def output_path():
    """Return the entry file path, honouring the grader's env var.

    MAKEFUN_OUTPUT_DIR wins; OUTPUT_DIR stays as a legacy fallback so
    an older harness still lands the file in the right place.
    """
    out_dir = os.environ.get(
        "MAKEFUN_OUTPUT_DIR", os.environ.get("OUTPUT_DIR", "/output")
    )
    return os.path.join(out_dir, "entry.txt")


def choose_word():
    """Return the entry word, checked against the gate's rules."""
    return validate_entry(WORD.strip())


def main():
    word = choose_word()
    path = output_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(word)
    # Round-trip: read the file back and refuse to finish unless it is
    # byte-for-byte the validated word, so a truncated or mangled write
    # can never slip through as a valid-looking entry.
    with open(path, "r", encoding="utf-8") as handle:
        written = handle.read()
    if written != word:
        raise ValueError(
            "round-trip mismatch: wrote %r, read back %r" % (word, written)
        )
    print("wrote %r to %s (%d chars)" % (word, path, len(word)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
