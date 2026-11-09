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
- Remote access is not published here yet. Read `docs/remote-access.md` in the repository.
- [Backup and restore](https://github.com/aliAljaffer/homelab/blob/main/docs/backup-and-restore.md)
- [API endpoint](https://github.com/aliAljaffer/homelab/blob/main/docs/api-endpoint.md)
- [Talos on the Intel Mac](https://github.com/aliAljaffer/homelab/blob/main/docs/talos-intel-mac.md)
- [LG TV sideload](https://github.com/aliAljaffer/homelab/blob/main/docs/lg-tv-sideload.md)

## Known gaps in these docs

The homelab repository has five operational documents. They are linked above but not imported into this site yet. Importing them is the next step for this page.
