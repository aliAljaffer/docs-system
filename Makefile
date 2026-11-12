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

brand:
	rm -rf .cache/brand brand
	gh repo clone aliAljaffer/branding .cache/brand -- --quiet --depth 1 --branch main --filter=blob:none --sparse
	git -C .cache/brand config credential.helper ''
	git -C .cache/brand config --add credential.helper '!gh auth git-credential'
	git -C .cache/brand sparse-checkout set export
	mkdir brand
	tar -C .cache/brand/export -c --exclude README.md --exclude 'plate-*' --exclude portfolio.css --exclude og . | tar -x -C brand

serve:
	python3 -m http.server -d site 8000

.PHONY: setup check build brand serve
