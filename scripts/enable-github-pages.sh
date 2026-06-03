#!/usr/bin/env bash
# Jednorazowe włączenie GitHub Pages (build_type=workflow).
# Wymaga: gh CLI, gh auth login, rola admin na repo.
set -euo pipefail

REPO="${1:-kris1pl/ai-research-forestry}"

if gh api "repos/${REPO}/pages" --silent 2>/dev/null; then
  echo "GitHub Pages już włączone dla ${REPO}"
  gh api "repos/${REPO}/pages" --jq '{url, build_type, status}'
  exit 0
fi

echo "Włączam GitHub Pages (workflow) dla ${REPO}..."
gh api --method POST "repos/${REPO}/pages" -f build_type=workflow
echo "OK. Teraz: Actions → Deploy Forestry Wiki (Quartz) → Re-run all jobs"
