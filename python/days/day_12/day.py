import sys
import re
from typing import List, Set
from loguru import logger
from dataclasses import dataclass
from icecream import ic
from functools import reduce
from itertools import cycle
from math import lcm
from itertools import combinations, product, combinations_with_replacement
from more_itertools import distinct_permutations
from tqdm import tqdm

from typing import Tuple, List, Dict, Any, Optional

logger.add(
    sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO"
)


@dataclass
class Row:
    row: str
    groups: List[int]


class Day:
    def __init__(self):
        ex_input = """
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""

        input_ = open("days/day_12/input.txt").read()
        lines = [x for x in ex_input.strip().splitlines() if x]
        self.rows = []

        for line in lines:
            row, int_str = line.strip().split(" ")
            ints = [int(x) for x in int_str.split(",")]
            self.rows.append(Row(row, ints))

    def part_1(self):
        sum = 0

        for row in tqdm(self.rows):
            valid_arrangements = self._get_valid_arrangements_2(row.row, row.groups)
            ic(valid_arrangements)
            sum += valid_arrangements

        return sum

    def _get_valid_arrangements_2(self, row, groups):
        total_trues = sum(groups)
        missing_trues = total_trues - row.count("#")
        missing_falses = row.count("?") - missing_trues

        valid_arrangements_count = 0

        for perm in tqdm(
            distinct_permutations("".join("#" * missing_trues + "." * missing_falses))
        ):
            perm = "".join(perm)
            current_row = ""
            p_idx = 0

            for char in row:
                if char == "?":
                    current_row += perm[p_idx]
                    p_idx += 1
                else:
                    current_row += char

            chunks = [len(x) for x in current_row.split(".") if x]
            if chunks == groups:
                valid_arrangements_count += 1

        return valid_arrangements_count

    def _get_valid_arrangements(self, row, groups):
        question_idxs = []
        bad_idxs = []
        for idx, char in enumerate(row):
            if char == "?":
                question_idxs.append(idx)
            elif char == "#":
                bad_idxs.append(idx)

        comb_len = sum(groups) - len(bad_idxs)

        str_groups = self._get_question_groups(row)
        combinations_per_group = {
            group: self._get_combinations(group) for group in str_groups
        }

        valid_combinations = 0
        for comb in combinations(question_idxs, comb_len):
            idxs = sorted(list(comb) + bad_idxs)
            valid_combinations += 1 if self._is_valid_bad_idxs(idxs, groups) else 0

        return valid_combinations

    def _get_combinations(self, group):
        size = group.count("?")
        combinations = list(product("#.", repeat=size))
        ic(combinations)

        combs = {}
        for comb in combinations:
            gs = {}

            out = True
            group_start = -1

            for idx, char in enumerate(comb):
                if char == "#" and out:
                    out = False
                    group_start = idx

                if char != "#" and not out:
                    out = True
                    g_l = idx - group_start

                    if g_l in gs:
                        gs[g_l] += 1
                    else:
                        gs[g_l] = 1

            if not out:
                g_l = len(comb) - group_start
                if g_l in gs:
                    gs[g_l] += 1
                else:
                    gs[g_l] = 1

            key = "-".join(sorted([":".join([str(k), str(v)]) for k, v in gs.items()]))

            if key in combs:
                combs[key] += 1
            else:
                combs[key] = 1

        ic(combs)

    def _get_question_groups(self, row):
        group_starts = []
        group_ends = []

        if row[0] == "?":
            group_starts.append(0)

        for idx, char in enumerate(row):
            if idx == 0:
                continue
            if char == "?" and row[idx - 1] != "?":
                group_starts.append(idx - 1)

            if char != "?" and row[idx - 1] == "?":
                group_ends.append(idx - 1)

        if row[-1] == "?":
            group_ends.append(len(row) - 1)

        str_groups = {}
        for idx_0, idx_1 in zip(group_starts, group_ends):
            group = row[idx_0 : idx_1 + 2]

            if group in str_groups:
                str_groups[group] += 1
            else:
                str_groups[group] = 1

        return str_groups

    def _is_valid_bad_idxs(self, idxs, groups):
        # build gap-only list
        new_list = []
        for idx, num in enumerate(idxs):
            if idx == 0:
                new_list.append(num)
                continue

            if num != idxs[idx - 1] + 1:
                new_list.append(idxs[idx - 1])
                new_list.append(num)

        new_list.append(idxs[-1])

        real_groups = []
        for idx in range(0, len(new_list), 2):
            real_groups.append(new_list[idx + 1] - new_list[idx] + 1)

        return real_groups == groups

    def part_2(self):
        rows = self._transform_rows(self.rows)
        rows = [rows[0]]

        chunks = [x for x in rows[0].row.split(".")]
        chunk_count = {c: chunks.count(c) for c in set(chunks)}

        ic(rows[0].row)
        ic(chunk_count)

        chunk_analysis = {}

        for chunk, count in chunk_count.items():
            valid_chunk_combinations = self._get_valid_chunk_combinations(chunk)
            valid_chunk_combinations = self._remove_impossible_combinations(
                valid_chunk_combinations, rows[0].groups
            )
            chunk_analysis[chunk] = {
                "count": count,
                "combinations": valid_chunk_combinations,
            }

        options = self._select_valid_options(chunk_analysis, rows[0].groups)
        ic(options)

    def _select_valid_options(self, chunk_analysis, groups):
        result = []

        for chunk, data in chunk_analysis.items():
            chunk_combinations = []
            for item in data["combinations"].keys():
                groups = item.split("-")

                chunk_combinations.append({})
                for group in groups:
                    if not group:
                        chunk_combinations[-1][0] = 1
                        continue

                    g_len, repeat = group.split(":")
                    chunk_combinations[-1][g_len] = repeat

            choices = list(
                combinations_with_replacement(
                    range(len(chunk_combinations)), data["count"]
                )
            )

            result.append([chunk, chunk_combinations, choices])

        ic(r[0] for r in result)
        ic(list(product(*[r[2] for r in result])))

    def _remove_impossible_combinations(self, combinations, groups):
        groups = {c: groups.count(c) for c in set(groups)}

        possible_combinations = {}
        for combination, count in combinations.items():
            gs = combination.split("-")
            lens = [int(x.split(":")[0]) for x in gs if x]

            if any(x not in groups for x in lens):
                continue
            else:
                possible_combinations[combination] = count

        return possible_combinations

    def _get_valid_chunk_combinations(self, chunk):
        if "?" not in chunk:
            return {f"{len(chunk)}:{1}": 1}

        combination_lenght = chunk.count("?")
        q_combs = list(product("#.", repeat=combination_lenght))
        combs = {}

        for q_comb in q_combs:
            comb = ""

            q_idx = 0
            for char in chunk:
                if char == "?":
                    comb += q_comb[q_idx]
                    q_idx += 1

                else:
                    comb += char

            out = True
            group_start = -1
            gs = {}

            for idx, char in enumerate(comb):
                if char == "#" and out:
                    out = False
                    group_start = idx

                if char != "#" and not out:
                    out = True
                    g_l = idx - group_start

                    if g_l in gs:
                        gs[g_l] += 1
                    else:
                        gs[g_l] = 1

            if not out:
                g_l = len(comb) - group_start
                if g_l in gs:
                    gs[g_l] += 1
                else:
                    gs[g_l] = 1

            key = "-".join(
                reversed(sorted([":".join([str(k), str(v)]) for k, v in gs.items()]))
            )

            if key in combs:
                combs[key] += 1
            else:
                combs[key] = 1

        return combs

    def _transform_rows(self, rows):
        final_rows = []
        for row in rows:
            final_rows.append(Row("?".join([row.row] * 5), row.groups * 5))

        return final_rows


def day():
    day = Day()
    # print(f"day_12: {day.part_1()}, {day.part_2()}")
    print(f"day_12: {day.part_2()}")
