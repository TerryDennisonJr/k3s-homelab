# Family Map

## Working Directory

Run the commands below from this project's directory. From the
`k3s-homelab` repository root:

```bash
cd family-map
```

Paths such as `deployment/` and `family-mapper/` are relative to this
working directory. Removing the nested `.git` directory does not change
these paths.

## Setup

1. Create a Google service account and download its JSON key.
2. Save the key as `deployment/gcp_creds/gcp_service_account.json`.
3. Share the Google spreadsheet with the service account's email address.
4. Build and push the image if you changed the application:

```bash
docker buildx build --platform linux/amd64 \
  -t infinitiq502004/family-map:1.1.6 \
  --push -f deployment/Dockerfile .
```

The image tag must match `image.repository` in `family-mapper/values.yaml`.

For local Python runs, set the credential path on your host:

```bash
export APP_ENV=local
export GOOGLE_APPLICATION_CREDENTIALS="$PWD/deployment/gcp_creds/gcp_service_account.json"
```

Kubernetes uses `/deployment/gcp_creds/gcp_service_account.json` inside
the CronJob container. That mount path is independent of the repository's
location on your host.

## Create Namespace and Secret

Keep the JSON file in `deployment/gcp_creds/`, which is ignored by Git
and excluded from the Docker build context. Never commit it or paste its
contents into Helm values. The CronJob mounts it from a Kubernetes Secret.

```bash
kubectl create namespace family-map --dry-run=client -o yaml | kubectl apply -f -

kubectl create secret generic google-service-account -n family-map \
  --from-file=gcp_service_account.json=deployment/gcp_creds/gcp_service_account.json \
  --dry-run=client -o yaml | kubectl apply -f -
```

The Secret key `gcp_service_account.json` becomes the filename at the
container's credential mount path.

## Create or Update CronJob

```bash
helm upgrade --install denn-map ./family-mapper \
  -n family-map -f family-mapper/values.yaml
```

## Manually Deploy Job from CronJob

```bash
kubectl create job --from=cronjob/family-mapper -n family-map \
  gsheet-run-$(date +%Y%m%d%H%M%S)
```

## Teardown

```bash
helm uninstall denn-map -n family-map
kubectl delete secret google-service-account -n family-map
```
