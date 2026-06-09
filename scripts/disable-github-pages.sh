#!/usr/bin/env bash
# Wyłączenie publicznego GitHub Pages dla tego repo (wiki jest na GCP + IAP).
# Wymaga: gh CLI, gh auth login, rola admin na repo.
set -euo pipefail

REPO="${1:-kris1pl/ai-research-forestry}"

if ! command -v gh >/dev/null 2>&1; then
  echo "Brak gh CLI. Zainstaluj: https://cli.github.com/"
  echo ""
  echo "Ręcznie w przeglądarce:"
  echo "  https://github.com/${REPO}/settings/pages"
  echo "  → Unpublish site / Source: None"
  exit 1
fi

if ! gh api "repos/${REPO}/pages" --silent 2>/dev/null; then
  echo "GitHub Pages nie są włączone dla ${REPO} (lub brak uprawnień)."
  exit 0
fi

echo "Wyłączam GitHub Pages dla ${REPO}..."
gh api --method DELETE "repos/${REPO}/pages"
echo "OK. Sprawdź: curl -sI https://kris1pl.github.io/ai-research-forestry/  → powinno być 404"
