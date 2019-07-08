import itertools
import random
import sys
import os
import json
import csv

COMMON_FIELD = "common_attributes"
INTERESTS_FIELD = "interests"


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
    If there is an interest shared by 2 or more members (or if not randomly choose a few items), make it show up here.
    """
    return [postprocess_match(match) for match in matches]


def intersect_n_lists(lists):
    """
    Returns a set containing elements that are common across all lists in the containing list passed in to this function.
    """
    assert lists
    intersection = set(lists[0])
    sets = [set(list_) for list_ in lists]
    for _set in sets:
        intersection = intersection & _set

    return intersection


def preprocess_interests(match):
    """
    Replaces the comma-delimited interests list, with a list of interests, and accumulates them across everyone in the group.
    Every interest is normalized, to ensure duplicates are not accidentally overcounted later.
    """
    list_of_all_interests = [
        person[INTERESTS_FIELD].split(",") for person in match
    ]

    flattened_interest_list = [
        normalize_word(item) for list_ in list_of_all_interests for item in list_
    ]

    return flattened_interest_list


def generate_common_attributes(match_object, all_interests):
    """
    @param all_interests - A list of all interests that everyone in the match has.
    @param match_object - A list of people, with a list of common interests.
    @return match_object - The given match_object, with a populated common attributes field.
    If there is an interest shared by everyone in the match, it is added to the common interest list.
    Otherwise, a few random interests that one or more people have, are added to the common interest list.
    """
    intersection = intersect_n_lists(all_interests)
    generated_interests = []
    if intersection:
        for item in intersection:
            generated_interests.append(item)
    all_interests_without_duplicates = list(set(all_interests))

    # Allow up to 5 things to talk about, consisting of some common interests, and some randomly chosen ones
    count_uncommon_interests = 5 - len(generated_interests)

    for i in range(count_uncommon_interests):
        generated_interests.append(random.choice(
            all_interests_without_duplicates))
    return generated_interests


def normalize_word(word):
    return word.strip().lower()


def postprocess_match(match):
    assert match

    match_object = {"matches": match}
    all_fields = match[0].keys()

    # Represents fields that contain just one element, as opposed to a field like interests
    single_item_fields = {}
    for field in all_fields:
        if field == INTERESTS_FIELD:
            all_interests = preprocess_interests(match)
            generated_interests = generate_common_attributes(
                match_object, all_interests)
            dict_upsert_list(match_object, COMMON_FIELD, generated_interests)
        else:
            for person in match:
                dict_upsert_list(single_item_fields, field, person[field])

    # print(json.dumps(single_item_fields, indent=4, sort_keys=True))
    for single_item_field, value in single_item_fields.items():
        for item in value:
            # Checks if a particular item, e.g. school is present more than once
            # If yes, add it to the common_attributes column
            if value.count(item) > 1:
                dict_upsert_list(match_object, COMMON_FIELD, item)

    if COMMON_FIELD in match_object:
        match_object[COMMON_FIELD] = list(set(match_object[COMMON_FIELD]))

        if "" in match_object[COMMON_FIELD]:
            match_object[COMMON_FIELD].remove("")

    return match_object


def dict_upsert_list(dictionary, field, item):
    """
    Appends an item to a list in a dictionary, or creates a new list with that item for a particular field.
    The item can be a list, in which case, all elements from the list are appended.
    """
    if field in dictionary:
        dictionary[field] = dictionary[field] + [item]
    else:
        if type(item) is list:
            dictionary[field] = item
        else:
            dictionary[field] = [item]


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(
            "See usage in README. Must provide path to file with a newline-delimited list of interns, group size, and output file.",
            file=sys.stderr)
        sys.exit(os.EX_USAGE)

    input_filename = sys.argv[1]
    intern_list = preprocess_data(input_filename)

    group_size = int(sys.argv[2])
    matches = generate_intern_pairings(intern_list=intern_list,
                                       group_size=group_size)

    postprocessed_matches = postprocess_matches(matches)

    output_serialized = json.dumps(
        postprocessed_matches, indent=4, sort_keys=True)

    output_filename = sys.argv[3]
    with open(output_filename, 'w') as output_file:
        output_file.write(output_serialized)
