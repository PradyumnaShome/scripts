from jinja2 import Environment, FileSystemLoader, select_autoescape
import json
import os
import sys

TEMPLATES_DIRECTORY = "templates"
TEMPLATE_MATCHES = "matches.html"
ARG_MISSING_ERROR_MESSAGE = "See usage in README. Must provide path to JSON output of matching algorithm, and output HTML file."

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(ARG_MISSING_ERROR_MESSAGE, file=sys.stderr)
        sys.exit(os.EX_USAGE)

    env = Environment(loader=FileSystemLoader(TEMPLATES_DIRECTORY),
                      autoescape=select_autoescape(['html', 'xml']))

    generated_matches_filename = sys.argv[1]

    matches = None
    with open(generated_matches_filename) as generated_matches_file:
        matches = json.load(generated_matches_file)

    template = env.get_template(TEMPLATE_MATCHES)

    output_filename = sys.argv[2]

    with open(output_filename, 'w') as file:
        file.write(template.render(list_matches=matches))
