# 2. Configuration

Goal: Store settings in ConfigMaps and Secrets, then attach them to workloads.

## ConfigMaps

- A ConfigMap stores variables.
- A ConfigMap stores config files up to 1 MiB.
- For larger files, store the data in a volume.

Create a ConfigMap from a literal value or from an env file:

```bash
kubectl create cm <name> --from-literal=key=value
kubectl create cm <name> --from-env-file=path/to/file
```

Attach a ConfigMap to a deployment as environment variables:

```bash
kubectl set env --from=configmap/my_cm deploy/mydeploy
kubectl set env --from=configmap/my_cm deploy/mydeploy --prefix="TF_VAR_"
```

## Secrets

!!! warning "Secrets are not encrypted"
    A Secret stores data in base64 encoding. Anyone who reads the Secret can decode it.

A Secret has one of three types:

| Type | Use for |
|---|---|
| `generic` | Values such as passwords |
| `tls` | TLS keys |
| `docker-registry` | Container registry credentials |

Create a TLS Secret:

```bash
kubectl create secret tls my-tls-keys --cert=tls/my.crt --key=tls/my.key
```

Use a Secret in one of these ways:

| Use | How |
|---|---|
| Variables | Run `kubectl set env`. |
| Files | Mount the Secret as a volume. |
| Registry pulls | Add the Secret under `pod.spec.imagePullSecrets`. |

To limit file access, set `defaultMode: 0400` under the Secret volume.

## Exam tips

- Know `kubectl create cm`, `kubectl set env`, and `kubectl create secret tls`.
- Use `kubectl set env` for variables and volume mounts for files.
- Set `defaultMode: 0400` to restrict Secret file permissions.

[Next: Multi-container pods](03-multi-container-pods.md)
