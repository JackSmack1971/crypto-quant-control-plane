import json
import sys
import tempfile
import shutil
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from verify_scaffold import validate
from research_manifest import build_manifest

class ControlPlaneTests(unittest.TestCase):
    def test_baseline(self):
        self.assertGreaterEqual(len(validate()["files"]), 15)

    def test_manifest_is_deterministic(self):
        self.assertEqual(build_manifest(), build_manifest())

    def test_manifest_detects_source_changes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "project"
            shutil.copytree(ROOT, root)
            initial = build_manifest(root)
            (root / "AGENTS.md").write_text((root / "AGENTS.md").read_text() + "\nnew policy\n")
            changed = build_manifest(root)
            self.assertNotEqual(initial, changed)

    def test_missing_methodology_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "project"
            shutil.copytree(ROOT, root)
            (root / "methodologies/09-strategy-execution-methodology.md").unlink()
            with self.assertRaises(AssertionError):
                validate(root)

    def test_missing_specialist_skill_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "project"
            shutil.copytree(ROOT, root)
            (root / ".agents/skills/onchain-investigation/SKILL.md").unlink()
            with self.assertRaises(AssertionError):
                validate(root)

    def test_agent_write_instruction_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "project"
            shutil.copytree(ROOT, root)
            path = root / ".codex/agents/verifier.toml"
            path.write_text(path.read_text().replace("Do not edit files", "Edit files as needed"))
            with self.assertRaises(AssertionError):
                validate(root)

    def test_unknown_config_key_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "project"
            shutil.copytree(ROOT, root)
            path = root / ".codex/config.toml"
            path.write_text(path.read_text() + "\nunsupported_setting = true\n")
            with self.assertRaises(AssertionError):
                validate(root)

    def test_network_relaxation_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "project"
            shutil.copytree(ROOT, root)
            path = root / ".codex/config.toml"
            path.write_text(path.read_text().replace("network_access = false", "network_access = true"))
            with self.assertRaises(AssertionError):
                validate(root)

    def test_added_finance_server_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "project"
            shutil.copytree(ROOT, root)
            path = root / ".codex/config.toml"
            path.write_text(path.read_text() + '\n[mcp_servers.exchange]\nurl = "https://example.org/mcp"\n')
            with self.assertRaises(AssertionError):
                validate(root)

if __name__ == "__main__":
    unittest.main()
