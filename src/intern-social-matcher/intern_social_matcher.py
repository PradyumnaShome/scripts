import itertools
import random
import sys
import os
import json
import csv

COMMON_FIELD = "common_attributes"


def preprocess_data(input_filename):
    """
    Takes in a a CSV file with interns and useful information, and generates a list of objects which comprise all the fields for a person.
    """
    intern_list = []
    with open(sys.argv[1]) as intern_list_file:
        csv_reader = csv.DictReader(intern_list_file)
        for index, row in enumerate(csv_reader):
            if index == 0:
                pass
            intern_list.append(row)
        return intern_list


def generate_intern_pairings(intern_list, group_size):
    """
    Partitions the given list of interns into groups of given size.
    """
    random.shuffle(intern_list)

    intern_count = len(intern_list)
    return [
        intern_list[x:x + group_size]
        for x in range(0, intern_count, group_size)
    ]


def postprocess_matches(matches):
    """
    Add interesting information.
    If there is an interest shared by 2 or more members, make it show up here.
    """
    return [postprocess_match(match) for match in matches]


def intersect_n_lists(lists):
    assert lists
    intersection = set(lists[0])
    sets = [set(list_) for list_ in lists]
    for _set in sets:
        intersection = intersection & _set

    return intersection


def preprocess_interests(match):
    list_of_all_interests = [
        person["interests"].split(",") for person in match
    ]
    flattened_interest_list = [
        item for list_ in list_of_all_interests for item in list_
    ]
    return flattened_interest_list


def postprocess_match(match):
    assert match

    match_object = {"matches": match}
    all_fields = match[0].keys()

    single_item_fields = {}
    for field in all_fields:
        if field == "interests":
            all_interests = preprocess_interests(match)
            intersection = intersect_n_lists(all_interests)
            if intersection:
                for item in intersection:
                    dict_upsert_list(match_object, COMMON_FIELD, item)
            else:
                all_interests_without_duplicates = list(set(all_interests))
                # Pick count_interests / 3 things at random, as things to talk about
                for i in range(len(all_interests_without_duplicates) / 2):
                    dict_upsert_list(match_object, COMMON_FIELD,
                                     random.choice(all_interests))
        else:
            for person in match:
                dict_upsert_list(single_item_fields, field, person[field])

    for key, value in single_item_fields.items():
        for item in value:
            # Checks if a particular item, e.g. school is present more than once
            # If yes, add it to the common_attributes column
            if value.count(item) > 1:
                dict_upsert_list(match_object, COMMON_FIELD, item)
                break

    return match_object


def dict_upsert_list(dictionary, field, item):
    """
    Appends an item to a list in a dictionary, or creates a new list with that item for a particular field.
    """
    if field in dictionary:
        dictionary[field].append(item)
    else:
        dictionary[field] = [item]


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(
            "See usage in README. Must provide path to file with a newline-delimited list of interns, and group size.",
            file=sys.stderr)
        sys.exit(os.EX_USAGE)

    input_filename = sys.argv[1]
    intern_list = preprocess_data(input_filename)

    group_size = int(sys.argv[2])
    matches = generate_intern_pairings(intern_list=intern_list,
                                       group_size=group_size)

    postprocessed_matches = postprocess_matches(matches)

    print(json.dumps(postprocessed_matches, indent=4, sort_keys=True))
