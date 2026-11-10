# 7. Ingress, Gateway API, and network policies

Goal: Route external traffic, and limit traffic between namespaces.

## Ingress

Ingress gives external access to resources inside the cluster.

The Gateway API replaces Ingress. The exam still requires Ingress.

Ingress path types:

- `Exact`: matches the path exactly.
- `Prefix`: matches paths that start with the given prefix.

## Gateway API

The Gateway API defines routing and traffic management policies. It supports:

- UDP, TCP, and gRPC.
- Traffic splitting and mirroring.
- WebSocket protocols.

## NetworkPolicy

A NetworkPolicy limits traffic between namespaces.

To find the pods a policy applies to, check the labels in its ingress and egress rules.

## Istio

Istio is a service mesh. It suits microservices, and large or complex environments.

## Exam tips

- Know the difference between `Exact` and `Prefix` path types.
- Check the labels in ingress and egress rules to see which pods a NetworkPolicy affects.

[Next: Storage](08-storage.md)
