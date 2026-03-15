"""Unit tests for src/ocr/core.py — pure function tests.

Uses stdlib unittest (no external dependencies).
Run:  python -m unittest tests.test_ocr_core -v
"""

import json
import tempfile
import unittest
from pathlib import Path

from src.ocr.core import (
    ParsedResponse,
    VLMResult,
    _parse_run_number,
    compute_prompt_hash,
    detect_provider,
    estimate_cost,
    find_or_create_run_folder,
    list_run_folders,
    load_run_state,
    next_run_number,
    parse_vlm_response,
    save_run_state,
)

# ── detect_provider ─────────────────────────────────────────────


class TestDetectProvider(unittest.TestCase):
    def test_claude_prefix(self):
        self.assertEqual(detect_provider("claude-sonnet-4"), "anthropic")

    def test_gemini_prefix(self):
        self.assertEqual(detect_provider("gemini-3.1-pro"), "google")

    def test_gpt_prefix(self):
        self.assertEqual(detect_provider("gpt-5"), "openai")

    def test_o_series(self):
        self.assertEqual(detect_provider("o4-mini"), "openai")

    def test_unknown_defaults_openai(self):
        self.assertEqual(detect_provider("some-custom-model"), "openai")


# ── compute_prompt_hash ─────────────────────────────────────────


class TestComputePromptHash(unittest.TestCase):
    def test_deterministic(self):
        h1 = compute_prompt_hash("test prompt")
        h2 = compute_prompt_hash("test prompt")
        self.assertEqual(h1, h2)

    def test_length(self):
        h = compute_prompt_hash("anything")
        self.assertEqual(len(h), 8)

    def test_hex_chars(self):
        h = compute_prompt_hash("check hex")
        self.assertTrue(all(c in "0123456789abcdef" for c in h))

    def test_different_inputs(self):
        h1 = compute_prompt_hash("prompt A")
        h2 = compute_prompt_hash("prompt B")
        self.assertNotEqual(h1, h2)


# ── estimate_cost ────────────────────────────────────────────────


class TestEstimateCost(unittest.TestCase):
    def test_known_model(self):
        cost = estimate_cost("gemini-2.5-flash", 1_000_000, 1_000_000)
        self.assertIsNotNone(cost)
        self.assertAlmostEqual(cost, 0.15 + 0.60)

    def test_unknown_model(self):
        self.assertIsNone(estimate_cost("nonexistent-model", 1000, 1000))

    def test_zero_tokens(self):
        cost = estimate_cost("gemini-2.5-flash", 0, 0)
        self.assertEqual(cost, 0.0)


# ── parse_vlm_response ──────────────────────────────────────────


SAMPLE_RESPONSE = """\
=== JSONL ===
{"br": "Demat", "fr": "Bonjour"}
{"br": "Kenavo", "fr": "Au revoir"}
=== /JSONL ===

=== RAPPORT ===
Statut: OK
Score: 85
Remarques: Bonne qualité
Observations workflow: aucune
=== /RAPPORT ===
"""


class TestParseVlmResponse(unittest.TestCase):
    def test_valid_response(self):
        result = parse_vlm_response(SAMPLE_RESPONSE)
        self.assertEqual(result["statut"], "OK")
        self.assertEqual(result["score"], "85")
        self.assertEqual(result["remarques"], "Bonne qualité")
        self.assertEqual(result["observations"], "aucune")
        self.assertIn('{"br": "Demat"', result["jsonl"])
        self.assertIn('{"br": "Kenavo"', result["jsonl"])

    def test_empty_string(self):
        result = parse_vlm_response("")
        self.assertEqual(result["jsonl"], "")
        self.assertEqual(result["statut"], "Impossible")
        self.assertEqual(result["score"], "N/A")

    def test_missing_jsonl_block(self):
        text = """\
=== RAPPORT ===
Statut: Difficultés
Score: 40
Remarques: Image floue
Observations workflow: améliorer le contraste
=== /RAPPORT ===
"""
        result = parse_vlm_response(text)
        self.assertEqual(result["jsonl"], "")
        self.assertEqual(result["statut"], "Difficultés")
        self.assertEqual(result["score"], "40")

    def test_missing_rapport_block(self):
        text = """\
=== JSONL ===
{"br": "test", "fr": "test"}
=== /JSONL ===
"""
        result = parse_vlm_response(text)
        self.assertNotEqual(result["jsonl"], "")
        self.assertEqual(result["statut"], "Impossible")  # default

    def test_score_with_percent(self):
        text = """\
=== JSONL ===
=== /JSONL ===

=== RAPPORT ===
Statut: OK
Score: 90%
Remarques: ok
Observations workflow: aucune
=== /RAPPORT ===
"""
        result = parse_vlm_response(text)
        self.assertEqual(result["score"], "90")  # % stripped


# ── _parse_run_number ────────────────────────────────────────────


class TestParseRunNumber(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(_parse_run_number("0001-20260314-1624"), 1)

    def test_large_number(self):
        self.assertEqual(_parse_run_number("0042-20260101-0000"), 42)

    def test_invalid_format(self):
        self.assertIsNone(_parse_run_number("not-a-run-folder"))

    def test_wrong_digit_count(self):
        self.assertIsNone(_parse_run_number("01-20260314-1624"))

    def test_empty(self):
        self.assertIsNone(_parse_run_number(""))


# ── Run folder management ────────────────────────────────────────


class TestRunFolderManagement(unittest.TestCase):
    def test_save_and_load_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            state = {"prompt_hash": "abc12345", "status": "in_progress"}
            save_run_state(tmp_path, state)
            loaded = load_run_state(tmp_path)
            self.assertIsNotNone(loaded)
            self.assertEqual(loaded["prompt_hash"], "abc12345")

    def test_load_missing_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertIsNone(load_run_state(Path(tmp)))

    def test_load_corrupt_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "run_state.json").write_text("not json", encoding="utf-8")
            self.assertIsNone(load_run_state(Path(tmp)))

    def test_list_run_folders_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(list_run_folders(Path(tmp)), [])

    def test_list_run_folders_sorted(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            (tmp_path / "0002-20260102-1200").mkdir()
            (tmp_path / "0001-20260101-1000").mkdir()
            (tmp_path / "0003-20260103-1400").mkdir()
            (tmp_path / "not-a-run").mkdir()
            folders = list_run_folders(tmp_path)
            self.assertEqual(len(folders), 3)
            self.assertEqual(folders[0].name, "0001-20260101-1000")
            self.assertEqual(folders[2].name, "0003-20260103-1400")

    def test_next_run_number_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(next_run_number(Path(tmp)), 1)

    def test_next_run_number_increments(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "0003-20260103-1400").mkdir()
            self.assertEqual(next_run_number(Path(tmp)), 4)

    def test_find_or_create_new_folder(self):
        with tempfile.TemporaryDirectory() as tmp:
            model_dir = Path(tmp) / "book" / "model"
            run_dir = find_or_create_run_folder(
                model_dir, "book", "model", "test prompt"
            )
            self.assertTrue(run_dir.exists())
            self.assertTrue((run_dir / "extracted").is_dir())
            self.assertTrue((run_dir / "reports" / "extraction").is_dir())
            self.assertTrue((run_dir / "prompt.md").exists())
            state = load_run_state(run_dir)
            self.assertEqual(state["status"], "in_progress")
            self.assertEqual(state["prompt_hash"], compute_prompt_hash("test prompt"))

    def test_find_or_create_reuses_matching_hash(self):
        with tempfile.TemporaryDirectory() as tmp:
            model_dir = Path(tmp) / "book" / "model"
            run1 = find_or_create_run_folder(model_dir, "book", "model", "same prompt")
            run2 = find_or_create_run_folder(model_dir, "book", "model", "same prompt")
            self.assertEqual(run1, run2)

    def test_find_or_create_new_on_different_prompt(self):
        with tempfile.TemporaryDirectory() as tmp:
            model_dir = Path(tmp) / "book" / "model"
            run1 = find_or_create_run_folder(model_dir, "book", "model", "prompt v1")
            run2 = find_or_create_run_folder(model_dir, "book", "model", "prompt v2")
            self.assertNotEqual(run1, run2)

    def test_find_or_create_reuses_completed(self):
        with tempfile.TemporaryDirectory() as tmp:
            model_dir = Path(tmp) / "book" / "model"
            run1 = find_or_create_run_folder(model_dir, "book", "model", "my prompt")
            state = load_run_state(run1)
            state["status"] = "completed"
            save_run_state(run1, state)

            run2 = find_or_create_run_folder(model_dir, "book", "model", "my prompt")
            self.assertEqual(run1, run2)


if __name__ == "__main__":
    unittest.main()
