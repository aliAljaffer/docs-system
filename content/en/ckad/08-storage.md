# 8. Storage

Goal: Use pod volumes to store data outside a container's own filesystem.

## Why not ephemeral storage

Ephemeral storage is bad for shared data. It is host-bound, so only one application instance can access it.

## Pod volumes

Use the `volumes` property of the pod to define storage.

!!! note "Pod volumes are not always persistent volumes"
    A pod volume does not have to be a persistent volume.

Mount each pod volume with `volumeMounts` under `pod.spec.containers`.

For per-pod persistent storage, see [StatefulSets](05-workload-types.md).

## Exam tips

- Define volumes under `pod.spec.volumes`.
- Attach volumes to containers with `volumeMounts` under `pod.spec.containers`.

[Next: Exam tips and tools](09-exam-tips-and-tools.md)
