# 5. Workload types

Goal: Choose the right workload for one-time jobs, stateful apps, node agents, and autoscaling.

## Jobs

Use a Job for one-time work, such as backups and calculations.

- Set `restartPolicy: Never`.
- Set `spec.ttlSecondsAfterFinished`. The notes recommend it.

## StatefulSets

A StatefulSet keeps the identity of its pods after a restart. Use it for databases.

Use a StatefulSet when you need:

- Stable, unique network identifiers.
- Stable, persistent storage.
- Ordered, graceful deployment and scaling.
- Ordered and automated rolling updates.

Storage uses `volumeClaimTemplate`. It creates a PVC that connects to a PV.

!!! warning "Deleting a StatefulSet keeps its volumes"
    Deleting a StatefulSet does not delete the volumes it uses.

Helm charts make StatefulSets easier to manage.

## DaemonSets

A DaemonSet runs one pod on every node.

- Use a DaemonSet for a node agent, such as a logging or monitoring agent.
- The DaemonSet adds or removes pods as nodes join or leave the cluster.

## Autoscaling

A HorizontalPodAutoscaler watches usage statistics. When usage passes a threshold, it adds replicas.

## Exam tips

- Use a Job with `restartPolicy: Never` for one-time work.
- Use a StatefulSet when pods need stable identity or stable storage.
- A DaemonSet runs one pod per node.

[Next: Services](06-services.md)
