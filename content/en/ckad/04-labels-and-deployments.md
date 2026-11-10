# 4. Labels and deployments

Goal: Group resources with labels and manage a deployment's scaling and rollouts.

## Labels

- `kubectl create deploy` adds the label `app=<deployment_name>` by default.
- `kubectl run` adds the label `run=<pod_name>` by default.

Find all resources with a label:

```bash
kubectl get all --selector app=my_app
```

!!! warning "Labels do not pass to managed resources"
    Adding a label to an existing deployment does not add it to the resources the deployment manages.

Add a label with `key=value`. Remove a label by adding a minus sign after its key:

```bash
kubectl label <resource> <name> <key>=<value>
kubectl label <resource> <name> <key>-
```

## Annotations

Annotations store notes. Labels group resources. Use annotations for notes only.

```bash
kubectl annotate deploy <deployment_name> newnote="My new note"
```

## Scaling

A deployment scales through a ReplicaSet.

```bash
kubectl scale deploy <deployment_name> --replicas=4
```

## Rolling updates

Set these fields under `rollingUpdate`:

- `maxSurge`: how many extra pods can run during an update, above the desired count.
- `maxUnavailable`: how many pods can be unavailable during an update.

Both fields accept an integer or a percentage.

## Rollout history and undo

An update creates a new ReplicaSet with the updated properties. Kubernetes keeps the old ReplicaSet and sets its replicas to 0.

```bash
kubectl rollout history deploy/<deployment_name>
kubectl rollout undo deploy/<deployment_name> --to-revision=1
```

## Exam tips

- Use `kubectl get all --selector` to find resources by label.
- Remember that a label added to a deployment does not reach the resources it manages.
- Know the difference between `maxSurge` and `maxUnavailable`.

[Next: Workload types](05-workload-types.md)
