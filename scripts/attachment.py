"""Emit a Hermes Desktop attachment line for each verified local file."""
import argparse
import sys
from pathlib import Path


def attachment_line(value):
    path = Path(value).expanduser().resolve(strict=True)
    if not path.is_file() or any(char in path.as_posix() for char in "\r\n"):
        raise ValueError(f"Expected a single-line path to a regular file: {value!r}")
    with path.open("rb") as stream:
        stream.read(1)
    return "MEDIA:" + path.as_posix()


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="+")
    args = parser.parse_args()
    try:
        lines = [attachment_line(value) for value in args.files]
    except (OSError, ValueError, RuntimeError) as error:
        parser.exit(1, f"Attachment check failed: {error}\n")
    print("\n".join(lines))
