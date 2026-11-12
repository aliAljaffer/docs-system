# 6. Services

Goal: Expose a set of pods inside or outside the cluster.

A Service exposes a set of pods. It forwards traffic with round-robin load balancing. A selector chooses the pods.

## Service types

- `ClusterIP`: the default type. It exposes the Service inside the cluster.
- `NodePort`: opens a specific port on the node. The port forwards to the Service IP on the cluster network.
- `LoadBalancer`: creates an external load balancer for applications in a public cloud.
- `ExternalName`: redirects at the DNS level. Useful during a migration.
- Headless Service: a `ClusterIP` Service with `clusterIP: None`. It lets you reach pods directly. Used with StatefulSets.

## Create a Service

Expose a deployment on a port:

```bash
kubectl expose deploy/<deployment_name> --port <N>
kubectl create service <type> <name> --tcp=<port>:<targetPort>
```

Port fields:

- `targetPort`: the port on the container.
- `port`: the port where the Service is reachable.
- `nodePort`: the external port for a `NodePort` Service.

## DNS

A Service has this DNS name:

```text
<service-name>.<namespace>.svc.<cluster-name>
```

Use the full DNS name when the two pods are in different namespaces.

## Exam tips

- Expose deployments with `kubectl expose`. Most exam tasks expose deployments.
- Know that `targetPort` is the container port and `port` is the Service port.
- Use the full DNS name across namespaces.

[Next: Ingress and network policies](07-ingress-and-network-policies.md)
