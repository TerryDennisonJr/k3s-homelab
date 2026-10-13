#!/bin/bash

kubectl create namespace family-map
kubectl create secret generic google-service-account -n family-map \
  --from-file=deployment/gcp_creds/gcp_service_account.json
