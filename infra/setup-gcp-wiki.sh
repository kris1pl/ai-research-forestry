#!/usr/bin/env bash
# Idempotent setup: GCS + External HTTPS LB + IAP + WIF for Conifervision wiki.
# Run from repo root with: bash infra/setup-gcp-wiki.sh
set -euo pipefail

PROJECT_ID="${PROJECT_ID:-conifer-vision01}"
REGION="${REGION:-europe-central2}"
BUCKET="${BUCKET:-conifervision-wiki-prod}"
WIKI_HOSTNAME="${WIKI_HOSTNAME:-wiki.conifervision.com}"
GITHUB_REPO="${GITHUB_REPO:-kris1pl/ai-research-forestry}"
SA_NAME="${SA_NAME:-wiki-deployer}"
WIF_POOL="${WIF_POOL:-github-pool}"
WIF_PROVIDER="${WIF_PROVIDER:-github-provider}"
READERS_GROUP="${READERS_GROUP:-wiki-readers@conifervision.com}"

# LB + Cloud Run resource names
IP_NAME="wiki-lb-ip"
URL_MAP_NAME="wiki-url-map"
CR_SERVICE="wiki-frontend"
CR_SA_NAME="wiki-runtime"
BACKEND_SERVICE="wiki-backend-service"
SERVERLESS_NEG="wiki-serverless-neg"
AR_REPO="wiki"
HTTP_REDIRECT_MAP="wiki-http-redirect"
SSL_CERT_NAME="wiki-ssl-cert"
HTTPS_PROXY_NAME="wiki-https-proxy"
HTTP_PROXY_NAME="wiki-http-proxy"
HTTPS_RULE_NAME="wiki-https-rule"
HTTP_RULE_NAME="wiki-http-rule"

SA_EMAIL="${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"
PROJECT_NUMBER="$(gcloud projects describe "$PROJECT_ID" --format='value(projectNumber)')"

echo "==> Project: $PROJECT_ID ($PROJECT_NUMBER)"

gcloud config set project "$PROJECT_ID"

echo "==> Enabling APIs..."
gcloud services enable \
  compute.googleapis.com \
  iap.googleapis.com \
  storage.googleapis.com \
  certificatemanager.googleapis.com \
  cloudresourcemanager.googleapis.com \
  iam.googleapis.com \
  iamcredentials.googleapis.com \
  sts.googleapis.com \
  run.googleapis.com \
  artifactregistry.googleapis.com \
  cloudbuild.googleapis.com

echo "==> GCS bucket gs://${BUCKET}..."
if gcloud storage buckets describe "gs://${BUCKET}" &>/dev/null; then
  echo "    Bucket exists"
else
  gcloud storage buckets create "gs://${BUCKET}" \
    --location="$REGION" \
    --uniform-bucket-level-access
fi
gcloud storage buckets update "gs://${BUCKET}" --no-public-access-prevention-enforced 2>/dev/null || true
# Ensure no public IAM
gcloud storage buckets remove-iam-policy-binding "gs://${BUCKET}" \
  --member=allUsers --role=roles/storage.objectViewer 2>/dev/null || true

echo "==> Reserved global IP..."
if gcloud compute addresses describe "$IP_NAME" --global &>/dev/null; then
  echo "    IP exists"
else
  gcloud compute addresses create "$IP_NAME" --global
fi
LB_IP="$(gcloud compute addresses describe "$IP_NAME" --global --format='value(address)')"
echo "    LB IP: $LB_IP  (DNS A record: ${WIKI_HOSTNAME} -> ${LB_IP})"

CR_SA_EMAIL="${CR_SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"
IMAGE="${REGION}-docker.pkg.dev/${PROJECT_ID}/${AR_REPO}/frontend:latest"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

echo "==> Artifact Registry..."
if ! gcloud artifacts repositories describe "$AR_REPO" --location="$REGION" &>/dev/null; then
  gcloud artifacts repositories create "$AR_REPO" \
    --repository-format=docker \
    --location="$REGION" \
    --description="Conifervision wiki nginx"
fi

echo "==> Cloud Run runtime SA ${CR_SA_EMAIL}..."
if ! gcloud iam service-accounts describe "$CR_SA_EMAIL" &>/dev/null; then
  gcloud iam service-accounts create "$CR_SA_NAME" \
    --display-name="Wiki Cloud Run (reads GCS)"
fi
gcloud storage buckets add-iam-policy-binding "gs://${BUCKET}" \
  --member="serviceAccount:${CR_SA_EMAIL}" \
  --role="roles/storage.objectViewer" 2>/dev/null || true

echo "==> Build & push wiki-nginx image..."
gcloud auth configure-docker "${REGION}-docker.pkg.dev" --quiet
docker build -t "$IMAGE" "${REPO_ROOT}/infra/wiki-nginx"
docker push "$IMAGE"

echo "==> Cloud Run service ${CR_SERVICE}..."
if ! gcloud run services describe "$CR_SERVICE" --region="$REGION" &>/dev/null; then
  gcloud run deploy "$CR_SERVICE" \
    --image="$IMAGE" \
    --region="$REGION" \
    --service-account="$CR_SA_EMAIL" \
    --set-env-vars="GCS_BUCKET=${BUCKET}" \
    --port=8080 \
    --no-allow-unauthenticated \
    --quiet
else
  gcloud run deploy "$CR_SERVICE" \
    --image="$IMAGE" \
    --region="$REGION" \
    --service-account="$CR_SA_EMAIL" \
    --set-env-vars="GCS_BUCKET=${BUCKET}" \
    --port=8080 \
    --no-allow-unauthenticated \
    --quiet
fi

echo "==> Serverless NEG + backend service (IAP)..."
if ! gcloud compute network-endpoint-groups describe "$SERVERLESS_NEG" --region="$REGION" &>/dev/null; then
  gcloud compute network-endpoint-groups create "$SERVERLESS_NEG" \
    --region="$REGION" \
    --network-endpoint-type=serverless \
    --cloud-run-service="$CR_SERVICE"
fi

if ! gcloud compute backend-services describe "$BACKEND_SERVICE" --global &>/dev/null; then
  gcloud compute backend-services create "$BACKEND_SERVICE" \
    --load-balancing-scheme=EXTERNAL_MANAGED \
    --global
  gcloud compute backend-services add-backend "$BACKEND_SERVICE" \
    --global \
    --network-endpoint-group="$SERVERLESS_NEG" \
    --network-endpoint-group-region="$REGION"
fi

echo "==> URL map (default -> backend service)..."
if ! gcloud compute url-maps describe "$URL_MAP_NAME" &>/dev/null; then
  gcloud compute url-maps create "$URL_MAP_NAME" \
    --default-service="$BACKEND_SERVICE"
else
  gcloud compute url-maps set-default-service "$URL_MAP_NAME" \
    --default-service="$BACKEND_SERVICE" \
    --global
fi

echo "==> Managed SSL certificate..."
if gcloud compute ssl-certificates describe "$SSL_CERT_NAME" --global &>/dev/null; then
  echo "    SSL cert exists"
else
  gcloud compute ssl-certificates create "$SSL_CERT_NAME" \
    --domains="$WIKI_HOSTNAME" \
    --global
fi

echo "==> HTTPS proxy + forwarding rule..."
if ! gcloud compute target-https-proxies describe "$HTTPS_PROXY_NAME" &>/dev/null; then
  gcloud compute target-https-proxies create "$HTTPS_PROXY_NAME" \
    --url-map="$URL_MAP_NAME" \
    --ssl-certificates="$SSL_CERT_NAME" \
    --global
fi
if ! gcloud compute forwarding-rules describe "$HTTPS_RULE_NAME" --global &>/dev/null; then
  gcloud compute forwarding-rules create "$HTTPS_RULE_NAME" \
    --load-balancing-scheme=EXTERNAL_MANAGED \
    --network-tier=PREMIUM \
    --address="$IP_NAME" \
    --target-https-proxy="$HTTPS_PROXY_NAME" \
    --ports=443 \
    --global
fi

echo "==> HTTP -> HTTPS redirect..."
if ! gcloud compute url-maps describe "$HTTP_REDIRECT_MAP" &>/dev/null; then
  gcloud compute url-maps import "$HTTP_REDIRECT_MAP" --global --source /dev/stdin <<EOF
name: ${HTTP_REDIRECT_MAP}
defaultUrlRedirect:
  redirectResponseCode: MOVED_PERMANENTLY_DEFAULT
  httpsRedirect: true
EOF
fi
if ! gcloud compute target-http-proxies describe "$HTTP_PROXY_NAME" &>/dev/null; then
  gcloud compute target-http-proxies create "$HTTP_PROXY_NAME" \
    --url-map="$HTTP_REDIRECT_MAP" \
    --global
fi
if ! gcloud compute forwarding-rules describe "$HTTP_RULE_NAME" --global &>/dev/null; then
  gcloud compute forwarding-rules create "$HTTP_RULE_NAME" \
    --load-balancing-scheme=EXTERNAL_MANAGED \
    --network-tier=PREMIUM \
    --address="$IP_NAME" \
    --target-http-proxy="$HTTP_PROXY_NAME" \
    --ports=80 \
    --global
fi

echo "==> IAP on backend service ${BACKEND_SERVICE}..."
# IAP requires OAuth consent screen (Internal) — configure once in Console if this fails.
gcloud compute backend-services update "$BACKEND_SERVICE" \
  --global \
  --iap=enabled 2>/dev/null || \
  echo "    WARN: Enable IAP in Console (Security -> IAP -> ${BACKEND_SERVICE}) after OAuth consent screen"

echo "==> IAP accessor for ${READERS_GROUP}..."
gcloud iap web add-iam-policy-binding \
  --project="$PROJECT_ID" \
  --resource-type=backend-services \
  --service="$BACKEND_SERVICE" \
  --member="group:${READERS_GROUP}" \
  --role="roles/iap.httpsResourceAccessor" \
  2>/dev/null || echo "    WARN: Group may not exist yet — create in Google Admin first"

echo "==> Deploy service account ${SA_EMAIL}..."
if ! gcloud iam service-accounts describe "$SA_EMAIL" &>/dev/null; then
  gcloud iam service-accounts create "$SA_NAME" \
    --display-name="Wiki GCS deployer (GitHub Actions)"
fi
gcloud storage buckets add-iam-policy-binding "gs://${BUCKET}" \
  --member="serviceAccount:${SA_EMAIL}" \
  --role="roles/storage.objectAdmin"
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:${SA_EMAIL}" \
  --role="roles/run.developer" \
  --condition=None 2>/dev/null || true

echo "==> Workload Identity Federation..."
if ! gcloud iam workload-identity-pools describe "$WIF_POOL" \
  --location=global --project="$PROJECT_ID" &>/dev/null; then
  gcloud iam workload-identity-pools create "$WIF_POOL" \
    --project="$PROJECT_ID" \
    --location=global \
    --display-name="GitHub Actions"
fi

if ! gcloud iam workload-identity-pools providers describe "$WIF_PROVIDER" \
  --workload-identity-pool="$WIF_POOL" --location=global --project="$PROJECT_ID" &>/dev/null; then
  gcloud iam workload-identity-pools providers create-oidc "$WIF_PROVIDER" \
    --project="$PROJECT_ID" \
    --location=global \
    --workload-identity-pool="$WIF_POOL" \
    --display-name="GitHub" \
    --attribute-mapping="google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.repository=assertion.repository,attribute.repository_owner=assertion.repository_owner" \
    --attribute-condition="assertion.repository_owner=='${GITHUB_REPO%%/*}'" \
    --issuer-uri="https://token.actions.githubusercontent.com"
fi

WIF_PROVIDER_FULL="projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/${WIF_POOL}/providers/${WIF_PROVIDER}"

gcloud iam service-accounts add-iam-policy-binding "$SA_EMAIL" \
  --project="$PROJECT_ID" \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/${WIF_POOL}/attribute.repository/${GITHUB_REPO}"

echo ""
echo "========== SETUP SUMMARY =========="
echo "LB IP (DNS A):     ${LB_IP}"
echo "Hostname:          ${WIKI_HOSTNAME}"
echo "Bucket:            gs://${BUCKET}"
echo "Cloud Run:         ${CR_SERVICE} (${REGION})"
echo "Backend service:   ${BACKEND_SERVICE}"
echo "Service account:   ${SA_EMAIL}"
echo ""
echo "GitHub Secrets (Settings -> Secrets and variables -> Actions):"
echo "  GCP_WORKLOAD_IDENTITY_PROVIDER=${WIF_PROVIDER_FULL}"
echo "  GCP_SERVICE_ACCOUNT=${SA_EMAIL}"
echo ""
echo "SSL cert status:"
gcloud compute ssl-certificates describe "$SSL_CERT_NAME" --global --format='yaml(managed.status,managed.domainStatus)'
echo "==================================="
