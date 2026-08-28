#!/usr/bin/env python3
"""
N-Queens Problem – Internship Submission
Author: Suresh Das
Date: 2026-08-28

Description:
    Solves the N-Queens problem using backtracking.
    Finds all possible ways to place N queens on an NxN chessboard
    such that no two queens threaten each other.

Usage:
    python n_queens.py --n 8
    python n_queens.py --n 4 --all
    python n_queens.py --n 10 --output solutions.txt

Objectives:
    - Represent board as a 2D array
    - Use backtracking to place queens safely
    - Ensure no two queens share row, column, or diagonal
    - Efficient constraint checking (O(1) per placement)
"""

import sys
import argparse
from typing import List, Optional


class NQueensSolver:
    """
    Solves the N-Queens problem using backtracking with O(1) conflict checks.
    """

    def __init__(self, n: int):
        self.n = n
        self.solutions = []  # List of all solutions (each as a list of column positions)
        self.board = []  # 2D representation for display
        self.reset_board()

    def reset_board(self):
        """Initialize the board with all empty cells."""
        self.board = [["." for _ in range(self.n)] for _ in range(self.n)]

    def solve(self, find_all: bool = True) -> List[List[int]]:
        """
        Find all solutions to the N-Queens problem.
        If find_all is True, find all solutions; otherwise, stop at the first.
        Returns a list of solutions, where each solution is a list of column indices
        (row index = position in list).
        """
        self.solutions = []
        self._backtrack(0, set(), set(), set(), find_all)
        return self.solutions

    def _backtrack(self, row: int, cols: set, diag1: set, diag2: set, find_all: bool):
        """
        Backtracking with O(1) conflict checks using sets.
        - row: current row to place queen
        - cols: columns already occupied
        - diag1: main diagonals (r - c) occupied
        - diag2: anti-diagonals (r + c) occupied
        """
        # Base case: all queens placed
        if row == self.n:
            # Store solution as column positions (row index = position in list)
            cols_used = sorted(list(cols))
            self.solutions.append(cols_used)
            return

        for col in range(self.n):
            # Check if placing a queen at (row, col) is safe
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue

            # Place queen
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)
            self.board[row][col] = "Q"

            # Recurse to next row
            self._backtrack(row + 1, cols, diag1, diag2, find_all)

            # Backtrack: remove queen
            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)
            self.board[row][col] = "."

            # If we only need one solution, stop after finding it
            if not find_all and self.solutions:
                return

    def display_solution(self, solution: List[int], show_board: bool = True) -> str:
        """
        Convert a solution (list of column positions) to a visual board.
        """
        n = self.n
        board = []
        for row, col in enumerate(solution):
            row_str = " ".join("Q" if col == c else "." for c in range(n))
            board.append(row_str)

        if show_board:
            header = f"\n{'=' * (n * 2 + 1)}"
            return header + "\n" + "\n".join(board) + header
        else:
            return f"[{', '.join(str(c + 1) for c in solution)}]"

    def display_solution_compact(self, solution: List[int]) -> str:
        """
        Display solution as a compact string: "Q at (row, col)"
        """
        return "[" + ", ".join(f"({i+1},{col+1})" for i, col in enumerate(solution)) + "]"

    def display_statistics(self) -> str:
        """
        Return statistics about the problem.
        """
        total = len(self.solutions)
        if total == 0:
            return f"No solutions found for {self.n}-Queens."

        # Get first solution for display
        first = self.solutions[0]

        return f"""
┌─────────────────────────────────────┐
│  N-Queens Problem Statistics        │
├─────────────────────────────────────┤
│  Board size         : {self.n} x {self.n}      │
│  Total solutions    : {total}                  │
│  First solution     : {self.display_solution_compact(first)} │
└─────────────────────────────────────┘
"""


def save_solutions_to_file(filename: str, solutions: List[List[int]], n: int) -> None:
    """Save all solutions to a text file."""
    try:
        with open(filename, "w") as f:
            f.write(f"N-Queens Problem: {n} Queens\n")
            f.write("=" * 40 + "\n")
            f.write(f"Total Solutions: {len(solutions)}\n\n")

            for idx, sol in enumerate(solutions, 1):
                f.write(f"Solution {idx}:\n")
                # Write board
                for row, col in enumerate(sol):
                    row_str = " ".join("Q" if col == c else "." for c in range(n))
                    f.write(row_str + "\n")
                f.write("\n" + "-" * 40 + "\n\n")

        print(f"💾 Solutions saved to: {filename}")
    except IOError as e:
        print(f"❌ Failed to save solutions: {e}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Solve the N-Queens problem using backtracking.")
    parser.add_argument(
        "--n",
        type=int,
        default=8,
        help="Size of the chessboard (default: 8)"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Find all solutions (default: find all solutions)"
    )
    parser.add_argument(
        "--first",
        action="store_true",
        help="Find only the first solution (faster for large N)"
    )
    parser.add_argument(
        "--output",
        help="Save all solutions to a text file"
    )
    parser.add_argument(
        "--display",
        choices=["board", "compact"],
        default="board",
        help="Display format for solutions (default: board)"
    )
    args = parser.parse_args()

    # Validate N
    if args.n < 1:
        print("❌ N must be at least 1.")
        sys.exit(1)

    if args.n > 20:
        print(f"⚠️  Warning: N={args.n} may take a long time to find all solutions.")

    # Determine if we find all or just one
    find_all = not args.first

    print(f"\n{'=' * 50}")
    print(f"👑 Solving {args.n}-Queens Problem")
    print(f"{'=' * 50}\n")

    # Create solver and solve
    solver = NQueensSolver(args.n)
    solutions = solver.solve(find_all=find_all)

    # Display statistics
    print(solver.display_statistics())

    # Show solutions if there are any
    if solutions:
        if args.display == "board":
            print("\n📊 First Solution (Board View):")
            print(solver.display_solution(solutions[0], show_board=True))
        else:
            print("\n📊 First Solution (Compact):")
            print(f"  {solver.display_solution_compact(solutions[0])}")

        # If find_all is True and we have multiple solutions, show count
        if find_all and len(solutions) > 1:
            print(f"\n📊 Found {len(solutions)} solutions total.")

        # Save to file if requested
        if args.output:
            save_solutions_to_file(args.output, solutions, args.n)
    else:
        print(f"\n❌ No solutions found for {args.n}-Queens.")

    print("\n" + "=" * 50)
    print("✅ Done!")


if __name__ == "__main__":
    # If no arguments, show help
    if len(sys.argv) == 1:
        print(__doc__)
        sys.exit(0)
    main()