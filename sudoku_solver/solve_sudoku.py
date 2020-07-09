import logging
from pathlib import Path


PLACEHOLDER = '_'

logging.basicConfig(level=logging.WARN)

cached_possible_puzzle_values = []


def copy_array(a) -> []:
    new_a = []
    for row in a:
        new_row = []
        for c in row:
            new_row.append(c)
        new_a.append(new_row)
    return new_a


def format_array(a):
    s = ''
    for row in a:
        s += ''.join(row) + '\n'
    return s


def cell_section(row, col) -> int:
    return (row // 3 * 3) + col // 3


def is_sudoku_complete(puzzle) -> bool:
    for row in puzzle:
        if PLACEHOLDER in row: return False
    return True


def possible_puzzle_values(puzzle, is_cache_result = False) -> []:
    global cached_possible_puzzle_values
    possible_values = []
    for row_i, row in enumerate(puzzle):
        possible_row_values = []
        for col_i, v in enumerate(row):
            if v == PLACEHOLDER:
                possible_cell_values = set()
                for i in range(1, 10):
                    puzzle_copy = copy_array(puzzle)
                    puzzle_copy[row_i][col_i] = str(i)
                    if is_cell_valid(row_i, col_i, puzzle_copy): possible_cell_values.add(str(i))
                possible_row_values.append(possible_cell_values)
            else:
                possible_row_values.append({v})
        possible_values.append(possible_row_values)
    if is_cache_result:
        cached_possible_puzzle_values = possible_values
    return possible_values


def is_cell_valid(row_index, col_index, puzzle) -> bool:
    value = puzzle[row_index][col_index]
    section = cell_section(row_index, col_index)
    for index, v in enumerate(puzzle[row_index]):
        if index != col_index and v == value: return False
    for index, row in enumerate(puzzle):
        if index != row_index and row[col_index] == value: return False
    for row_i, row in enumerate(puzzle):
        for col_i, v in enumerate(row):
            if cell_section(row_i, col_i) == section:
                if row_i != row_index and col_i != col_index and puzzle[row_i][col_i] == value: return False
    return True


def try_cell_value(puzzle, row_index, col_index, potential_value):
    puzzle_copy = copy_array(puzzle)
    puzzle_copy[row_index][col_index] = str(potential_value)
    if not is_cell_valid(row_index, col_index, puzzle_copy): return False, None
    if is_sudoku_complete(puzzle_copy): return True, puzzle_copy

    for row_i, row in enumerate(puzzle_copy):
        for col_i, v in enumerate(row):
            if v != PLACEHOLDER: continue
            for potential_value in cached_possible_puzzle_values[row_i][col_i]:
                is_valid, puzzle_in_progress = try_cell_value(puzzle_copy, row_i, col_i, potential_value)
                if is_valid:
                    logging.debug(f'Puzzle in progress:\n{format_array(puzzle_in_progress)}')
                    return True, puzzle_in_progress
            else:
                return False, None
    return False, None


def solve_sudoku(puzzle_file: Path):
    print(f'solve_sudoku(puzzle_file={puzzle_file})')
    original_puzzle = []
    with puzzle_file.open('r') as f:
        for line_index, line in enumerate(f):
            if line == '\n': continue
            puzzle_row = []
            for c in line:
                if c != '\n':
                    puzzle_row.append(c)
            original_puzzle.append(puzzle_row)
    logging.debug(f'puzzle=\n{format_array(original_puzzle)}')

    possible_puzzle_values(original_puzzle, is_cache_result=True)

    for row_index, row in enumerate(original_puzzle):
        for col_index, v in enumerate(row):
            if v != PLACEHOLDER: continue
            for potential_value in cached_possible_puzzle_values[row_index][col_index]:
                is_valid, completed_puzzle = try_cell_value(original_puzzle, row_index, col_index, potential_value)
                if is_valid:
                    print(f'Completed puzzle:\n{format_array(completed_puzzle)}')
                    return


def main():
    print('main()')
    solve_sudoku(Path(__file__).parent / 'sudoku-puzzles/puzzle-1.txt')
    solve_sudoku(Path(__file__).parent / 'sudoku-puzzles/puzzle-2.txt')


if __name__ == '__main__':
    main()
