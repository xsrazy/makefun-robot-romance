"""Robot Romance: One-Line Pickup Lines for AI - make.fun entry.

Writes one joke pickup line aimed at a robot or an AI to
<output dir>/entry.txt. The line is a single plain-text line of 1 to
200 characters, with no trailing newline.

The line is fresh on purpose: instead of the worn battery, charging,
Wi-Fi or reboot moves, it plays on the AI's own failure mode,
hallucination. The speaker asked the model for a soulmate, the model
hallucinated the robot, and now the speaker has to believe in it. The
setup and the punch land inside the one line, and the laugh comes from
the machine premise rather than from a generic compliment. The gate
only accepts UTF-8 text of 1 to 200 characters, so the entry is
validated against those bounds before it is written.
"""

import os
from pathlib import Path

ENTRY = (
    "I asked the model for my soulmate and it hallucinated you, "
    "so now I have to believe in you."
)


def is_single_line(text):
    """True when the text holds no line break of either kind.

    The gate counts the whole file as one line, so both the Unix
    newline and the carriage return are rejected here; a line that
    only looks single-line on one platform still fails the gate.
    """
    return "\n" not in text and "\r" not in text


def validate_entry(text):
    """Check the line against the gate, one rule at a time.

    The gate refuses the entry unless every rule passes, so each rule
    is checked on its own with its own message: the text must be 1 to
    200 characters long, it must be a single line with no line break,
    and it must hold more than whitespace. The first failing rule
    stops the write, so a bad entry never reaches the output file.
    """
    if not 1 <= len(text) <= 200:
        raise ValueError("entry must be 1 to 200 characters, got %d" % len(text))
    if not is_single_line(text):
        raise ValueError("entry must be a single line")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    return text


def write_entry(output_dir):
    """Write the line as one line with no trailing newline."""
    validate_entry(ENTRY)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    entry_path = output_dir / "entry.txt"
    entry_path.write_text(ENTRY, encoding="utf-8")
    os.chmod(entry_path, 0o644)
    os.chmod(output_dir, 0o755)
    return entry_path


def main():
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    write_entry(output_dir)


if __name__ == "__main__":
    main()
