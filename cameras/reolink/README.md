## Pre-Deployment Setup

Create the `cameras` namespace:

```bash
kubectl create namespace cameras
```

Run these commands from `cameras/reolink`. Copy the example and edit
`deployment/.env` locally with your MQTT and camera passwords:

```bash
cp deployment/.env.example deployment/.env
chmod 600 deployment/.env
```

Use `NAME=value` lines without quotes or `export`; this is a Kubernetes
env file, not a shell script. Git ignores `deployment/.env`. Do not put
passwords directly in `values.yaml` or commit generated Secret manifests.

Create the Secret in the same namespace as the Helm release (these
commands use `cameras`):

```bash
kubectl create secret generic frigate-credentials -n cameras \
  --from-env-file=deployment/.env --dry-run=client -o yaml | kubectl apply -f -
```

The chart's `envFromSecrets` passes the Secret values into the pod.
Frigate substitutes the `{FRIGATE_...}` placeholders at runtime. Exporting
variables in your local shell alone does not pass them into Kubernetes.

## Deploy or Update

The Frigate `nodeSelector` selects nodes labeled `node=worker2`.
K3s schedules its `svclb-*` pods separately. The Service's `lbpool` label
restricts those pods to nodes in the `cameras` load-balancer pool.
Before deploying, identify the selected node and label only that node:

```bash
kubectl get nodes -l node=worker2 -o wide
kubectl label node wnode2 svccontroller.k3s.cattle.io/lbpool=cameras
```

Replace `wnode2` if the first command reports a different node name.
If it reports multiple nodes, narrow the workload's `nodeSelector` to
the intended node as well. If the node already has an `lbpool` label,
check its existing services before replacing that label.

If your cluster already uses the `svccontroller.k3s.cattle.io/enablelb`
allow-list, the selected node must also have that label set to `true`.
Adding the first `enablelb` label changes eligibility for all ServiceLB
services in the cluster; the pool label above scopes this configuration
to the camera Service.

```bash
helm upgrade --install reolink-cameras blakeblackshear/frigate \
  -n cameras -f deployment/values.yaml
```

Verify that the camera ServiceLB pods run only on the selected node:

```bash
kubectl get pods -n kube-system \
  -l svccontroller.k3s.cattle.io/svcname=reolink-cameras-frigate,svccontroller.k3s.cattle.io/svcnamespace=cameras \
  -o wide
kubectl get service reolink-cameras-frigate -n cameras
```

This removes load-balancer redundancy: if that node is unavailable,
external camera access is unavailable too.

After changing passwords, update the Secret using the command above and
restart the release's deployment to reload the environment:

```bash
kubectl rollout restart deployment -n cameras \
  -l app.kubernetes.io/instance=reolink-cameras
```

## References

* [Youtube: NetworkChuck Reolink Setup (Docker)](https://www.youtube.com/watch?v=tbCKWX34_G4&t=2072s)

* [Frigate Helmchart](https://github.com/blakeblackshear/blakeshome-charts/tree/master/charts/frigate)

* [Frigate Camera Installation](https://docs.frigate.video/frigate/installation)
