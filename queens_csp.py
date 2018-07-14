__author__ = 'davide'

import sys
import random
import itertools as it
import operator
from functools import lru_cache
from collections import Counter


def start(board_size):
    def get_menaces(sol, row, col):
        return sum(attacks((r, c), (row, col))
                   for c, r in enumerate(sol, start=1))

    assignment = []
    pool = set()
    whole = set(range(1, board_size + 1))
    n = 1

    while n < board_size:
        els = [(col, get_menaces(assignment, col, n))
               for col in range(1, board_size + 1)]
        min_val = min(els, key=operator.itemgetter(1))[1]
        min_rows = {el[0] for el in els if el[1] == min_val}
        min_rows.difference_update(pool)
        if min_rows:
            element = random.sample(min_rows, 1)[0]
        else:
            els = whole - pool
            element = random.sample(els, 1)[0]
        assignment.append(element)
        pool.add(element)
        n += 1

    last_element = (whole - pool).pop()
    assignment.append(last_element)
    #nc = sum(num_of_conflicts(assignment, i)
    #         for i in range(1, board_size + 1))
    #print("Starting from", assignment, "\n#conflicts =", nc)
    return assignment


@lru_cache()
def attacks(pos_1, pos_2):
    return (pos_1[0] == pos_2[0] or
            pos_1[1] == pos_2[1] or
            abs(pos_1[0] - pos_2[0]) == abs(pos_1[1] - pos_2[1]))


def print_board(positions):
    for i in range(len(positions)):
        print("|", end="")
        for j in range(len(positions)):
            if positions[j] == i + 1:
                print("O", end="")
            else:
                print(" ", end="")
            print("|", end="")
        print()


def find_conflict_var(sol, board_size, last):
    def is_in_conflict(v):
        r = sol[v - 1]
        return any(v != c1 and attacks((r, v), (r1, c1))
                   for c1, r1 in enumerate(sol, start=1))

    pool = list(range(1, board_size + 1))
    if last is not None:
        pool.remove(last)
    while pool:
        v = random.choice(pool)
        if is_in_conflict(v):
            return v
        pool.remove(v)
    if last and is_in_conflict(last):
        return last


def set_value(sol, var, value):
    index = sol.index(value)
    sol[var - 1], sol[index] = value, sol[var - 1]


def num_of_conflicts(sol, var):
    row = sol[var - 1]
    return sum(var != c1 and attacks((row, var), (r1, c1))
               for c1, r1 in enumerate(sol, start=1))


def select_value(var, current, board_size):
    conflicts_vec = []
    current_o = current[:]
    for val in range(1, board_size + 1):
        set_value(current_o, var, val)
        conflicts_vec.append(num_of_conflicts(current_o, var))
        current_o = current[:]
    min_c = min(conflicts_vec)
    return random.choice([i for (i, v) in enumerate(conflicts_vec, start=1)
                          if v == min_c])


def min_conflicts(board_size, max_passi=100000):
    current = start(board_size)
    last = None
    iterable = range(max_passi) if max_passi > 0 else it.count()
    for it_count in iterable:
        #if it_count % 5 == 0:
            #cf = sum(num_of_conflicts(current, i) for i in range(1, board_size + 1))
            #print("Iteration", it_count, " # conflicts = ", cf)
        var = find_conflict_var(current, board_size, last)
        last = var
        if var is None:
            return current, it_count
        val = select_value(var, current, board_size)
        set_value(current, var, val)
    return None, max_passi


def main(board_size):
    solution, iters = min_conflicts(board_size, -1)
    if solution:
        print("Trovata!")
        print_board(solution)
        print("Iterazioni:", iters)
    else:
        print("Timeout")


if __name__ == "__main__":
    # N = int(sys.argv[1])
    main(8)