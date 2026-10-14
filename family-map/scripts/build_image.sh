#! /bin/bash

echo "Setting up Envars..."
sleep 3

export APP_ENV=local
export GOOGLE_APPLICATION_CREDENTIALS=/deployment/gcp_creds/gcp_service_account.json

docker buildx build \
  --platform linux/amd64 \
  -t infinitiq502004/family-map:1.1.6 \
  --push -f deployment/Dockerfile .

docker push infinitiq502004/family-map:1.1.6