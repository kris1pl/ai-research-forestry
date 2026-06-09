#!/usr/bin/env bash
# Print GitHub Actions secrets for deploy-wiki-gcp.yml (copy into repo Settings → Secrets).
set -euo pipefail

PROJECT_ID="${PROJECT_ID:-conifer-vision01}"
WIF_POOL="${WIF_POOL:-github-pool}"
WIF_PROVIDER="${WIF_PROVIDER:-github-provider}"
SA_EMAIL="${SA_EMAIL:-wiki-deployer@${PROJECT_ID}.iam.gserviceaccount.com}"

PROJECT_NUMBER="$(gcloud projects describe "$PROJECT_ID" --format='value(projectNumber)')"
WIF_PROVIDER_FULL="projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/${WIF_POOL}/providers/${WIF_PROVIDER}"

cat <<EOF
Add these GitHub Actions secrets for repo kris1pl/ai-research-forestry:

  Settings → Secrets and variables → Actions → New repository secret

Name: GCP_WORKLOAD_IDENTITY_PROVIDER
Value:
${WIF_PROVIDER_FULL}

Name: GCP_SERVICE_ACCOUNT
Value:
${SA_EMAIL}

Then re-run: Actions → Deploy Wiki (GCP + IAP) → Run workflow
EOF
