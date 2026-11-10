# 9. Exam tips and tools

Goal: Prepare for the exam environment and work faster in it.

These tips come from the author's own path to the CKAD (passed December 13, 2025), as part of the Kubestronaut journey.

## The exam environment

- The exam is online only.
- The environment can lag. Commands run slowly and keystrokes sometimes do not register.
- If latency is high, contact support about a re-take.
- The Killer.sh sessions feel the same or worse. Expect it.

!!! tip "Never pay full price"
    The CNCF offers discounts often, usually 40% to 60%. [Kube Promo](https://kube.promo) lists current promotions.

## Work faster

| Habit | How |
|---|---|
| Short `kubectl` | `alias k='kubectl'`. The exam environment sets this alias for you. |
| Do not write YAML from scratch | Add `--dry-run=client -o yaml` to `k create` or `k run`. Use `k get <resource> -o yaml` to copy an existing object. |
| Know one editor | Use `vim` and memorize block select and indent. |

## CKAD-specific tips

- Run a Minikube cluster on your own machine and experiment.
- Test a deployment or pod behind a `ClusterIP` service with `kubectl port-forward`.
- Use the short resource names: `cm` for ConfigMap, `sts` for StatefulSet. Run `kubectl api-resources` for the list.
- Create a ConfigMap or Secret straight from a file: `kubectl create cm <name> --from-file=path/to/file`.

## Documentation

- Learn to search and navigate the documentation. Each exam can include a question on a topic you did not study.
- Each question shows documentation links for its topic. Check them first, because they can hint at the method to use.
- `kubectl explain` is the in-terminal documentation.
- [kubespec.dev](https://kubespec.dev/) lists every field in the manifests for the current patch.
- The [Network Policy Editor](https://editor.networkpolicy.io/) helps with the policies in [lesson 7](07-ingress-and-network-policies.md).

## Practice

- Do the [Killercoda](https://killercoda.com/) scenarios. The author did them twice before the real exam.
- Your exam voucher includes a simulated environment. Run it and time yourself.

!!! info "More tips"
    For tips on the other Kubernetes exams (CKA, CKS, KCNA, KCSA), read the full [Kubestronaut write-up](https://alialjaffer.com/case-study/k8s-adventures-pt2/).

[Next: Exam-day checklist](10-exam-day-checklist.md)
