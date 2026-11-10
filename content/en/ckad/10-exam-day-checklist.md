# 10. Exam-day checklist

Goal: Confirm that you can run each core task from this course.

Check each item before the exam:

- [ ] Read a pod's spec with `kubectl get pod <pod-name> -o yaml`.
- [ ] Create a ConfigMap and attach it with `kubectl set env`.
- [ ] Create a TLS Secret with `kubectl create secret tls`.
- [ ] Set `defaultMode: 0400` on a Secret volume.
- [ ] Write an init container and a sidecar with `restartPolicy: Always`.
- [ ] Add and remove a label. Annotate a deployment.
- [ ] Scale a deployment with `kubectl scale`.
- [ ] Check rollout history and undo to a revision.
- [ ] Write a Job with `restartPolicy: Never`.
- [ ] Expose a deployment with `kubectl expose`.
- [ ] Explain the Service types, `targetPort`, `port`, and the DNS name.
- [ ] Explain the `Exact` and `Prefix` path types.
- [ ] Mount a pod volume with `volumeMounts`.
- [ ] Generate YAML with `kubectl create ... --dry-run=client -o yaml`.
- [ ] Look up any field with `kubectl explain` and the docs links shown on each question.

[Back to the course overview](index.md)
