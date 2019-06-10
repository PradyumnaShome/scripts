import itertools
import random
import sys
import os
import json


def get_intern_pairings(intern_list, group_size):
    random.shuffle(intern_list)

    intern_count = len(intern_list)
    return [
        intern_list[x:x + group_size]
        for x in range(0, intern_count, group_size)
    ]


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(
            "See usage in README. Must provide path to file with a newline-delimited list of interns, and group size.",
            file=sys.stderr)
        sys.exit(os.EX_USAGE)

    intern_list = None
    with open(sys.argv[1]) as intern_list_file:
        intern_list = intern_list_file.read().split("\n")

    group_size = int(sys.argv[2])

    pairings = get_intern_pairings(intern_list=intern_list,
                                   group_size=group_size)

    print(json.dumps(pairings, indent=4, sort_keys=True))
