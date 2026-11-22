"""Copy the runtime skill into an explicitly chosen Hermes skills directory."""

import argparse
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory


NAME = "hermes-engineering-workflow"
RUNTIME_FILES = (
    "SKILL.md",
    "LICENSE",
    "references/playbooks.md",
    "references/verification.md",
    "references/coordination.md",
    "references/model-routing.md",
    "references/maintenance.md",
    "references/delivery.md",
    "scripts/attachment.py",
    "assets/evidence.json",
    "scripts/check_evidence.py",
    "scripts/discover_models.py",
)


def install(source, skills_directory):
    skills_directory = skills_directory.expanduser().resolve()
    destination = skills_directory / NAME
    if destination.exists() or destination.is_symlink():
        raise FileExistsError(f"Skill already exists: {destination}")
    for relative in RUNTIME_FILES:
        path = source / relative
        if not path.is_file() or path.resolve() != source.resolve() / relative:
            raise ValueError(f"Missing or linked runtime file: {relative}")

    skills_directory.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(prefix=".install-", dir=skills_directory) as temporary:
        staged = Path(temporary) / NAME
        for relative in RUNTIME_FILES:
            path = staged / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source / relative, path)
        staged.rename(destination)
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skills_directory", type=Path)
    arguments = parser.parse_args()
    try:
        print(install(Path(__file__).resolve().parents[1], arguments.skills_directory))
    except (OSError, ValueError) as error:
        parser.exit(1, f"Install failed: {error}\n")


if __name__ == "__main__":
    main()
