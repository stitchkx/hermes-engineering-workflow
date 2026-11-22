import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from check_evidence import validate
from discover_models import discover
from install import NAME, RUNTIME_FILES, install


class PackageTests(unittest.TestCase):
    def test_metadata(self):
        metadata = (ROOT / "SKILL.md").read_text(encoding="utf-8").split("---\n", 2)
        self.assertEqual(metadata[0], "")
        self.assertIn(f"name: {NAME}\n", metadata[1])
        description = re.search(r"^description: (.+)$", metadata[1], re.M)[1]
        self.assertLessEqual(len(description), 60)
        self.assertTrue(metadata[2].strip())
        self.assertIn("Copyright (c) 2026 Lauren Tan", (ROOT / "LICENSE").read_text())

    def test_local_links_and_no_machine_data(self):
        runtime_links = set()
        private = re.compile(r"@session:|[A-Z]:[/\\](?:Users|hermes_project)|t_[0-9a-f]{8}\b")
        for path in ROOT.rglob("*.md"):
            if ".git" in path.parts:
                continue
            content = path.read_text(encoding="utf-8")
            self.assertIsNone(private.search(content), path)
            for link in re.findall(r"\[[^\]]+\]\(([^)]+)\)", content):
                if "://" in link or link.startswith("#"):
                    continue
                target = (path.parent / link.split("#", 1)[0]).resolve()
                self.assertTrue(target.is_file(), (path, link))
                if path.name == "SKILL.md" or path.parent.name == "references":
                    runtime_links.add(target.relative_to(ROOT).as_posix())
        self.assertTrue(runtime_links.issubset(RUNTIME_FILES))
        self.assertIn("references/model-routing.md", runtime_links)

    def test_install_cli_and_duplicate_refusal(self):
        with tempfile.TemporaryDirectory() as home:
            command = [sys.executable, str(ROOT / "scripts/install.py"), str(Path(home) / "skills")]
            first = subprocess.run(command, capture_output=True, text=True, check=True)
            destination = Path(first.stdout.strip())
            self.assertEqual(destination.name, NAME)
            installed = {p.relative_to(destination).as_posix() for p in destination.rglob("*") if p.is_file()}
            self.assertEqual(installed, set(RUNTIME_FILES))
            for name in RUNTIME_FILES:
                self.assertEqual((destination / name).read_bytes(), (ROOT / name).read_bytes())
            second = subprocess.run(command, capture_output=True, text=True, check=False)
            self.assertEqual(second.returncode, 1)
            self.assertIn("already exists", second.stderr)

    def test_incomplete_source_does_not_create_destination(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaises(ValueError):
                install(root, root / "skills")
            self.assertFalse((root / "skills" / NAME).exists())


class AttachmentTests(unittest.TestCase):
    def test_verified_paths_and_missing_member(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            report = root / "验收 清单.md"
            report.write_text("OK", encoding="utf-8")
            command = [sys.executable, str(ROOT / "scripts/attachment.py"), report.name]
            good = subprocess.run(
                command, cwd=root, capture_output=True, encoding="utf-8",
                env={**os.environ, "PYTHONIOENCODING": "cp1252"},
            )
            self.assertEqual(good.returncode, 0, good.stderr)
            self.assertEqual(good.stdout.strip(), "MEDIA:" + report.as_posix())
            bad = subprocess.run(command + ["missing.json"], cwd=root, capture_output=True)
            self.assertNotEqual(bad.returncode, 0)
            self.assertEqual(bad.stdout, b"")


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.record = json.loads((ROOT / "assets/evidence.json").read_text(encoding="utf-8"))

    def test_example_is_unverified(self):
        self.assertEqual(validate(self.record), [])
        self.assertIn("has not passed", " ".join(validate(self.record, require_pass=True)))

    def test_pass_requires_an_observation_and_evidence(self):
        check = self.record["checks"][0]
        check["status"] = "pass"
        self.assertEqual(len(validate(self.record, require_pass=True)), 2)
        check.update(observed="0", evidence="exit=0, stdout=0")
        self.assertEqual(validate(self.record, require_pass=True), [])

    def test_failure_and_duplicate_are_detected(self):
        check = self.record["checks"][0]
        check.update(status="fail", observed="30", evidence="stdout=30")
        self.assertEqual(validate(self.record), [])
        self.assertNotEqual(validate(self.record, require_pass=True), [])
        self.record["checks"].append(dict(check))
        self.assertIn("duplicate criterion", " ".join(validate(self.record)))

    def test_bad_shape_is_detected(self):
        self.assertNotEqual(validate(None), [])
        self.assertNotEqual(validate({"revision": "example", "checks": [{}]}), [])
        self.assertNotEqual(validate({"revision": "example", "checks": []}), [])


class ModelDiscoveryTests(unittest.TestCase):
    def test_magpie_and_variants_precede_active_and_other_providers(self):
        providers = {
            "alpha": {"models": ["general/chat"]},
            "magpie-messages": {"models": {"upstream/vision": {}}},
            "current": {"api_key": "synthetic-credential"},
            "magpie": {"models": ["upstream/coder", {"id": "upstream/coder"}]},
            "magpie-disabled": {"enabled": False, "models": ["unused"]},
        }
        routes = discover(providers, {"provider": "current", "default": "general/default"})
        self.assertEqual([route["provider"] for route in routes], ["magpie", "magpie-messages", "current", "alpha"])
        self.assertEqual(routes[0]["catalog_models"], ["upstream/coder"])
        self.assertEqual(routes[1]["catalog_models"], ["upstream/vision"])
        self.assertEqual(routes[2]["active_model"], "general/default")
        self.assertNotIn("synthetic-credential", json.dumps(routes))

    def test_no_magpie_falls_back_to_configured_default(self):
        routes = discover({"secondary": {"models": [{"model": "up/coder"}]}},
                          {"provider": "builtin", "default": "up/default"})
        self.assertEqual([route["provider"] for route in routes], ["builtin", "secondary"])
        self.assertEqual(routes[0]["active_model"], "up/default")
        self.assertEqual(routes[0]["catalog_models"], [])
        self.assertEqual(routes[1]["catalog_models"], ["up/coder"])
        self.assertEqual(discover({}, "up/model"), [])


if __name__ == "__main__":
    unittest.main()
