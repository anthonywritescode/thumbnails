all: bin/geckodriver build/style.css

venv: requirements.txt
	rm -rf venv
	virtualenv venv -ppython3
	venv/bin/pip install -rrequirements.txt
	venv/bin/pre-commit install -f --install-hooks

bin build:
	mkdir build

bin/geckodriver: Makefile
	./get-geckodriver.py v0.35.0
	touch $@

build/%.css: assets/scss/%.scss build venv
	venv/bin/pysassc -t compressed $< $@

clean:
	rm -rf bin build venv
