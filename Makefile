PYTHON ?= python3
PY := .venv/bin/python
BRAND_REF ?= terminal

setup:
	$(PYTHON) -m venv .venv
	$(PY) -m pip install -r requirements.txt

check:
	$(PY) check_sources.py

build:
	ZENSICAL=$(CURDIR)/.venv/bin/zensical $(PY) build.py
	$(PY) -m unittest discover -s tests

brand:
	rm -rf .cache/brand
	gh repo clone aliAljaffer/branding .cache/brand -- --quiet --depth 1 --branch $(BRAND_REF)
	rm -rf brand
	mkdir brand
	git -C .cache/brand archive HEAD | tar -x -C brand --exclude README.md

serve:
	python3 -m http.server -d site 8000

.PHONY: setup check build brand serve
