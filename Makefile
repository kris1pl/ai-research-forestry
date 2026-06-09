.PHONY: venv venv-recreate install extract-pdf llm-smoke ingest-paper build-wiki build-wiki-docker deploy-wiki-gcp serve-wiki serve-wiki-docker prepare-content

VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
REPO_ROOT := $(CURDIR)
DOCKER_NODE := node:22-bookworm-slim

# Na Apple Silicon użyj natywnego arm64 (unikaj Rosetta / x86_64 venv).
venv:
	arch -arm64 python3 -m venv $(VENV)

venv-recreate:
	rm -rf $(VENV)
	$(MAKE) venv install

install: venv
	$(PIP) install -U pip
	$(PIP) install -r requirements.txt

extract-pdf:
ifndef FILE
	$(error Użycie: make extract-pdf FILE=raw/papers/plik.pdf)
endif
	$(PYTHON) tools/extract_pdf_text.py $(FILE)

llm-smoke:
	$(PYTHON) -m tools.llm.smoke

ingest-paper:
ifndef FILE
	$(error Użycie: make ingest-paper FILE=raw/papers/plik.pdf [WRITE=1] [WIKI_ONLY=conifervision/sources/slug.md])
endif
	$(PYTHON) -m tools.ingest_paper $(FILE) $(if $(WRITE),--write,) $(if $(NO_WIKI),--no-wiki,) $(if $(WIKI_ONLY),--wiki-only $(WIKI_ONLY),)

# Lokalny build (wymaga Node >= 20.19; przy starszym Node użyj build-wiki-docker)
build-wiki:
	cd site && npm ci && npx quartz build

serve-wiki:
	cd site && npm ci && npx quartz build --serve

# Build przez Docker (Node 22) — gdy lokalny Node jest za stary
build-wiki-docker:
	docker run --rm -v "$(REPO_ROOT):/repo" -w /repo/site $(DOCKER_NODE) \
		bash -c "rm -rf content && cp -a ../conifervision content && npm ci && npx quartz build"

serve-wiki-docker:
	docker run --rm -p 8080:8080 -v "$(REPO_ROOT):/repo" -w /repo/site $(DOCKER_NODE) \
		bash -c "rm -rf content && cp -a ../conifervision content && npm ci && npx quartz build --serve --port 8080"

prepare-content:
	rm -rf site/content && cp -a conifervision site/content

# Build Quartz + rsync do GCS + odśwież Cloud Run (gdy CI nie zadziałał lub brak push)
deploy-wiki-gcp: build-wiki-docker
	gcloud storage rsync -r --delete-unmatched-destination-objects site/public gs://conifervision-wiki-prod
	gcloud run services update wiki-frontend --region=europe-central2 --project=conifer-vision01 \
		--update-env-vars="SYNC_TRIGGER=$$(date +%s)" --quiet
