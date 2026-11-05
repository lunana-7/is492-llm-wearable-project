import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "app/speech"))
from demo import review


class Review(unittest.TestCase):
    def test_discard_and_explicit_approval(self):
        with tempfile.TemporaryDirectory() as tmp:
            note = Path(tmp) / "note.txt"
            with patch("builtins.input", side_effect=["", ""]):
                self.assertFalse(review("Bring chart.", note))
            self.assertFalse(note.exists())
            with patch("builtins.input", side_effect=["Bring the revised chart.", "APPROVE"]):
                self.assertTrue(review("Bring chart.", note))
            self.assertEqual(note.read_text(), "Bring the revised chart.\n")
            with patch("builtins.input", side_effect=["Overwrite", "APPROVE"]):
                with self.assertRaises(FileExistsError):
                    review("Another draft", note)
