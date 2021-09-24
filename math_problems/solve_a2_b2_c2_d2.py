# Find integer solution to:
#     a + b = x
#     b + c = y
#     a + c = z
#     a + b + c = d

from collections import Counter
from pathlib import Path

import logging
import math
import time

logging.basicConfig(level=logging.DEBUG)

INIT = 0
MAX = 400
SOLUTIONS_FILE = f'solutions--max-{MAX}.csv'

SQUARES_MAP = {}


def calculate_squares(start, stop):
    squares = set()
    for i in range(start, stop):
        squares.add(i * i)
    return squares


def calculate_squares_map(start, stop):
    m = {}
    for i in range(start, stop):
        m[i] = i * i
    return m


def sum_of_squares(squares_map: {}, n: int, m: int, o: int = 0):
    # def sq(i):
    #     if SQUARES_MAP.get(i): return SQUARES_MAP.get(i)
    #     SQUARES_MAP[i] = i * i
    #     return SQUARES_MAP[i]
    # return sq(n) + sq(m) + sq(o)  # When max=300, time=4.5; When max=600, time=30.4,31.2,31.3;
    return squares_map[n] + squares_map[m] + squares_map[o]  # When max=300, time=2.3,2.3; When max=600, time=13.4,13.5,13.6,14.6;
    # return n * n + m * m + o * o  # When max=300, time=2.3,2.5; When max=600, time=14.5,14.6,14.9;


def is_solution_v1(a, b, c):
    def is_sum_of_squares_a_square(n, m, o=0):
        return math.sqrt(n * n + m * m + o * o).is_integer()

    # print(f'is_solution({a}, {b}, {c})')
    return is_sum_of_squares_a_square(a, b) \
           and is_sum_of_squares_a_square(b, c) \
           and is_sum_of_squares_a_square(a, c) \
           and is_sum_of_squares_a_square(a, b, c)


# def is_solution_v2(a, b, c, possible_squares):
#     return sum_of_squares(a, b) in possible_squares \
#            and sum_of_squares(b, c) in possible_squares \
#            and sum_of_squares(a, c) in possible_squares \
#            and sum_of_squares(a, b, c) in possible_squares


def is_solution_v2(a, b, c, possible_squares, squares_map):
    return sum_of_squares(squares_map, a, b) in possible_squares \
           and sum_of_squares(squares_map, b, c) in possible_squares \
           and sum_of_squares(squares_map, a, c) in possible_squares \
           and sum_of_squares(squares_map, a, b, c) in possible_squares


def save_solution(a, b, c, squares_map):
    with Path(SOLUTIONS_FILE).open('a+') as f:
        f.write(f'{a},{b},{c},{a*a},{b*b},{c*c},{sum_of_squares(squares_map, a, b, c)}\n')
        # f.write(f'{a},{b},{c},{sum_of_squares(squares_map, a, b)},{sum_of_squares(squares_map, b, c)},{sum_of_squares(squares_map, a, c)},{sum_of_squares(squares_map, a, b, c)}\n')


def solve(init, max, possible_squares, squares_map):
    print(f'solve()')
    number_of_solutions = 0
    for a in range(init, max):
        for b in range(a, max):
            for c in range(b, max):
                # if is_solution_v1(a, b, c):
                if is_solution_v2(a, b, c, possible_squares, squares_map):
                    save_solution(a, b, c, squares_map)
                    number_of_solutions += 1
    print(f'number_of_solutions={number_of_solutions}')


def analyze_squares(squares):
    print(f'analyze_squares()')
    last_digit_counts = Counter()
    for s in squares:
        last_digit_counts[s % 1000] += 1
    print(f'    last_digit_counts={sorted(last_digit_counts.items())}')
    print(f'    len(last_digit_counts)={len(last_digit_counts)}')

    # last_digits = [0, 1, 4, 5, 6, 9]
    last_digits = sorted(last_digit_counts.elements())
    last_digit_sums_counts = Counter()
    number_of_digits = len(last_digits)
    with Path('analyze-squares--last-digits.txt').open('w+') as f:
        for i in range(0, number_of_digits):
            for j in range(i, number_of_digits):
                for k in range(j, number_of_digits):
                    last_digit_sum = last_digits[i]+last_digits[j]+last_digits[k]
                    last_digit_sums_counts[last_digit_sum % 1000] += 1
                    f.write(f'{last_digits[i]}+{last_digits[j]}+{last_digits[k]}={last_digit_sum}\n')
    print(f'    last_digit_sums_counts={sorted(last_digit_sums_counts.items())}')
    print(f'    len(last_digit_sums_counts)={len(last_digit_sums_counts)}')


def main():
    print('main()')
    print(f'init: {INIT}, max={MAX}')


    Path(SOLUTIONS_FILE).write_text('a,b,c,a2,b2,c2,abc\n')
    # Path(SOLUTIONS_FILE).write_text('a,b,c,ab,bc,ac,abc\n')
    start_time = time.time()
    init, max = INIT, MAX
    possible_squares = calculate_squares(init, max * 2)
    analyze_squares(possible_squares)

    squares_map = calculate_squares_map(init, max)
    print(sorted(possible_squares))
    solve(init, max, possible_squares, squares_map)
    print(f'Total time: {time.time() - start_time} seconds')


if __name__ == '__main__':
    main()
