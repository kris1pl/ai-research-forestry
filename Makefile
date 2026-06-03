.PHONY: venv install extract-pdf build-wiki build-wiki-docker serve-wiki serve-wiki-docker

VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
REPO_ROOT := $(CURDIR)
DOCKER_NODE := node:22-bookworm-slim

venv:
	python3 -m venv $(VENV)

install: venv
	$(PIP) install -U pip
	$(PIP) install -r requirements.txt

extract-pdf:
ifndef FILE
	$(error Użycie: make extract-pdf FILE=raw/papers/plik.pdf)
endif
	$(PYTHON) tools/extract_pdf_text.py $(FILE)

# Lokalny build (wymaga Node >= 20.19; przy starszym Node użyj build-wiki-docker)
build-wiki:
	cd site && npm ci && npx quartz build

serve-wiki:
	cd site && npm ci && npx quartz build --serve

# Build przez Docker (Node 22) — gdy lokalny Node jest za stary
build-wiki-docker:
	docker run --rm -v "$(REPO_ROOT):/repo" -w /repo/site $(DOCKER_NODE) \
		bash -c "ln -sfn ../wiki content && npm ci && npx quartz build"

serve-wiki-docker:
	docker run --rm -p 8080:8080 -v "$(REPO_ROOT):/repo" -w /repo/site $(DOCKER_NODE) \
		bash -c "ln -sfn ../wiki content && npm ci && npx quartz build --serve --port 8080"
