PYTHON ?= python3
PY := .venv/bin/python

setup:
	$(PYTHON) -m venv .venv
	$(PY) -m pip install -r requirements.txt

check:
	$(PY) check_sources.py

build:
	ZENSICAL=$(CURDIR)/.venv/bin/zensical $(PY) build.py
	$(PY) -m unittest discover -s tests

serve:
	python3 -m http.server -d site 8000

.PHONY: setup check build serve
