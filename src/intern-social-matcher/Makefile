INPUT_FILE = interns_with_interests.csv
GENERATED_MATCHES_FILE = output.txt
RENDERED_FILE = index.html
GROUP_SIZE = 4

GENERATOR_SCRIPT = intern_social_matcher.py
RENDERER_SCRIPT = render_matches.py

.PHONY: all generate render clean

all: generate render

clean:
	rm $(GENERATED_MATCHES_FILE) $(RENDERED_FILE)

generate: $(INPUT_FILE) $(GENERATOR_SCRIPT)
	python3 $(GENERATOR_SCRIPT) $(INPUT_FILE) $(GROUP_SIZE) $(GENERATED_MATCHES_FILE)

render: $(GENERATED_MATCHES_FILE) $(RENDERER_SCRIPT)
	python3 $(RENDERER_SCRIPT) $(GENERATED_MATCHES_FILE) $(RENDERED_FILE)