# [Intern Social Matcher](https://pradyumnashome.github.io/scripts/src/intern-social-matcher/)

Get introduced to new interns every week.

Hosted [here](https://pradyumnashome.github.io/scripts/src/intern-social-matcher/).

## Usage

### Generate Matches

To generate matches, run

```bash
    python3 intern_social_matcher.py <intern_list_file> <group_size>
```

where

`intern_list_file` is a file with a list of interns, delimited by newlines.

`group_size` is the number of people you'd like to meet every time

### Render intern matching output

To render a web page, run

```bash
    python3 render_matches.py <matches_file> <output_file>
```

where

`matches_file` is a file with the output from the first step. It has generated matches in a double-nested JSON list.

`output_file` is the HTML file that is rendered from the matches.
