# 1. Pods

Goal: Read the YAML of a running pod and find each field.

## Inspect a pod

```bash
kubectl get pod <pod-name> -o yaml
```

## Pod spec layout

Pod settings sit under `pod.spec`. Use these paths:

| Path | Holds |
|---|---|
| `pod.spec.containers` | Containers in the pod |
| `pod.spec.containers.volumeMounts` | Mounts for pod volumes |
| `pod.spec.volumes` | Pod volumes |
| `pod.spec.imagePullSecrets` | Registry access credentials |

See [[containers]] for the container basics.

## Exam tips

- Run `kubectl get pod <pod-name> -o yaml` to read the full spec of a deployed pod.
- Know the `pod.spec` path for each field you need.

[Next: Configuration](02-configuration.md)
