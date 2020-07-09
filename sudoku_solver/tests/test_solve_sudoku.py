import unittest

from sudoku_solver import solve_sudoku


PUZZLE_1 = [
    ['5', '1', '_', '4', '6', '3', '9', '7', '2'],
    ['7', '6', '4', '2', '1', '9', '3', '5', '8'],
    ['9', '2', '3', '7', '8', '5', '1', '6', '4'],
    ['3', '8', '6', '9', '5', '4', '2', '1', '7'],
    ['1', '7', '9', '3', '2', '_', '_', '_', '5'],
    ['_', '_', '_', '1', '7', '_', '6', '_', '9'],
    ['_', '_', '1', '_', '4', '_', '_', '_', '3'],
    ['8', '_', '5', '_', '_', '_', '_', '2', '_'],
    ['2', '4', '_', '8', '_', '1', '_', '9', '6']
]


class MyTestCase(unittest.TestCase):
    def test_cell_section(self):
        self.assertEqual(solve_sudoku.cell_section(0, 0), 0)
        self.assertEqual(solve_sudoku.cell_section(0, 2), 0)
        self.assertEqual(solve_sudoku.cell_section(0, 3), 1)
        self.assertEqual(solve_sudoku.cell_section(0, 6), 2)
        self.assertEqual(solve_sudoku.cell_section(0, 8), 2)
        self.assertEqual(solve_sudoku.cell_section(5, 0), 3)
        self.assertEqual(solve_sudoku.cell_section(6, 0), 6)
        self.assertEqual(solve_sudoku.cell_section(8, 0), 6)
        self.assertEqual(solve_sudoku.cell_section(5, 5), 4)
        self.assertEqual(solve_sudoku.cell_section(5, 6), 5)
        self.assertEqual(solve_sudoku.cell_section(6, 5), 7)
        self.assertEqual(solve_sudoku.cell_section(6, 6), 8)
        self.assertNotEqual(solve_sudoku.cell_section(8, 8), 1)

    def test_is_sudoku_complete(self):
        puzzle = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
        self.assertTrue(solve_sudoku.is_sudoku_complete(puzzle))
        incomplete_puzzle = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, '_']
        ]
        self.assertFalse(solve_sudoku.is_sudoku_complete(incomplete_puzzle))
        self.assertFalse(solve_sudoku.is_sudoku_complete(PUZZLE_1))

    def test_possible_puzzle_values(self):
        puzzle = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
        possible_values = solve_sudoku.possible_puzzle_values(puzzle)
        self.assertListEqual(possible_values, [[{1}, {2}, {3}], [{4}, {5}, {6}], [{7}, {8}, {9}]])
        incomplete_puzzle = [
            ['1', '2', '3', '3'],
            ['4', '5', '6', '6'],
            ['7', '8', '9', '_']
        ]
        possible_values = solve_sudoku.possible_puzzle_values(incomplete_puzzle)
        self.assertListEqual(possible_values, [[{'1'}, {'2'}, {'3'}, {'3'}], [{'4'}, {'5'}, {'6'}, {'6'}], [{'7'}, {'8'}, {'9'}, {'1', '2', '4', '5'}]])

        possible_values = solve_sudoku.possible_puzzle_values(PUZZLE_1)
        self.assertListEqual(possible_values, [[{'5'}, {'1'}, {'8'}, {'4'}, {'6'}, {'3'}, {'9'}, {'7'}, {'2'}], [{'7'}, {'6'}, {'4'}, {'2'}, {'1'}, {'9'}, {'3'}, {'5'}, {'8'}], [{'9'}, {'2'}, {'3'}, {'7'}, {'8'}, {'5'}, {'1'}, {'6'}, {'4'}], [{'3'}, {'8'}, {'6'}, {'9'}, {'5'}, {'4'}, {'2'}, {'1'}, {'7'}], [{'1'}, {'7'}, {'9'}, {'3'}, {'2'}, {'6', '8'}, {'8', '4'}, {'8', '4'}, {'5'}], [{'4'}, {'5'}, {'2'}, {'1'}, {'7'}, {'8'}, {'6'}, {'3', '8', '4'}, {'9'}], [{'6'}, {'9'}, {'1'}, {'6', '5'}, {'4'}, {'6', '7', '2'}, {'8', '7', '5'}, {'8'}, {'3'}], [{'8'}, {'9', '3'}, {'5'}, {'6'}, {'9', '3'}, {'6', '7'}, {'7', '4'}, {'2'}, {'1'}], [{'2'}, {'4'}, {'7'}, {'8'}, {'3'}, {'1'}, {'7', '5'}, {'9'}, {'6'}]])


    def test_is_cell_valid(self):
        puzzle = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
        self.assertTrue(solve_sudoku.is_cell_valid(0, 0, puzzle))
        self.assertTrue(solve_sudoku.is_cell_valid(1, 1, puzzle))
        self.assertTrue(solve_sudoku.is_cell_valid(2, 2, puzzle))

        invalid_puzzle = [
            [2, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
        self.assertFalse(solve_sudoku.is_cell_valid(0, 0, invalid_puzzle))

        puzzle_copy = solve_sudoku.copy_array(PUZZLE_1)
        puzzle_copy[0][2] = '8'
        self.assertTrue(solve_sudoku.is_cell_valid(0, 2, puzzle_copy))


if __name__ == '__main__':
    unittest.main()
