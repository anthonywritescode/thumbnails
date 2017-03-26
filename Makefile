all: build/style.css

venv: requirements.txt
	rm -rf venv
	virtualenv venv -ppython3.6
	venv/bin/pip install -rrequirements.txt
	venv/bin/pre-commit install -f --install-hooks

build:
	mkdir build

build/%.css: assets/scss/%.scss build venv
	venv/bin/sassc -t compressed $< $@

clean:
	rm -rf venv build
