# Homelab

**Status:** Active

A Kubernetes homelab on Talos Linux, managed entirely through ArgoCD. The cluster runs the services I use every day: identity, passwords, DNS, media, notifications, and this documentation site.

## Stack

| Layer | Choice |
|---|---|
| OS | Talos Linux |
| Kubernetes | v1.36.2 |
| CNI and ingress | Cilium, Gateway API |
| Public entry | Cloudflare Tunnel Gateway |
| GitOps | ArgoCD, app-of-apps |
| Storage | Longhorn |
| Database | CloudNativePG |
| Identity | Keycloak |
| Metrics | Prometheus, Thanos, Grafana |
| Logs | Loki, Grafana Alloy |
| Secrets | Sealed Secrets, SOPS |

## Nodes

| Node | Role | Notes |
|---|---|---|
| cp0 | Control plane | MacBook Pro Mid-2012, custom Talos kernel |
| wrk0 | Control plane | Lenovo M920q |
| wrk1 | Control plane | Lenovo M920q |
| wrk2 | Worker | Lenovo M920q |
| wrk3 | Worker | Lenovo M920q |
| gpu | Worker, on demand | Ryzen 7 7800X3D, RTX 4070 Ti Super |

## Operations

The source repository is the source of truth. If a service is not in it, it does not exist on the cluster.

- [Repository](https://github.com/aliAljaffer/homelab)
- [Remote cluster access](remote-access.md)
- [Backup and restore](backup-and-restore.md)
- [Cluster API endpoint](api-endpoint.md)
- [Talos on the Intel Mac](talos-intel-mac.md)
- [LG TV sideload](lg-tv-sideload.md)

## Import status

These pages are copied from `docs/` in the repository by `sync.py`. Edit the repository, then run `sync.py`, not these pages.
