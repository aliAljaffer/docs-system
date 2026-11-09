# OpenZiti Operator

**Status:** Active

A Kubernetes operator that makes routine [OpenZiti](https://openziti.io) work simple. You describe an app, an identity, or a router in YAML. The operator creates the Ziti configs, services, policies, and identities, then checks that the result works and reports it in `status`.

It drives the Ziti Edge Management API. It does not install or run the Ziti controller. This is an independent community project, not an official OpenZiti or NetFoundry product.

**Release:** `v0.3.1`, API `v1alpha1`. Tested with Ziti controller and router v2.0.4 and Kubernetes v1.36.

## Stack

| Part | Choice |
|---|---|
| Language | Go 1.27 |
| Runtime | Kubernetes operator, controller-runtime |
| API | Ziti Edge Management API, `ziti.alialjaffer.com/v1alpha1` |
| Delivery | Helm chart, `ghcr.io/alialjaffer/openziti-operator` |
| Tests | envtest, kind end-to-end, Ginkgo |

## What it does

| You want to | You apply |
|---|---|
| Publish an app so authorized people can reach it | `ZitiApp` |
| Enroll or remove an identity | `ZitiIdentity` |
| Start a router on a VM or in a cluster | `ZitiRouter` |
| Take over resources built by hand | `managementPolicy: Adopt` or `Observe` |
| Log a workload in through a Ziti tunneler | `ZitiSidecar` |
| Expose an HTTP Ingress | Annotate it with `ziti.alialjaffer.com/expose: "true"` |
| Forward a local port to a Ziti service | `ZitiPortForward` |
| Log in with a certificate or a service account token | `ZitiCA` and `ZitiJwtSigner` |

For full control, there is one resource for every Ziti object.

## Start here

- [Repository](https://github.com/aliAljaffer/openziti-operator)
- [Releases](https://github.com/aliAljaffer/openziti-operator/releases)
- [Chart](https://github.com/aliAljaffer/openziti-operator/pkgs/container/charts%2Fziti-operator)
- [Install](install.md)
- [First app](first-app.md)
- [Compatibility](compatibility.md)

## Guides

- [Install](install.md), [First app](first-app.md), [Uninstall](uninstall.md)
- [Role scope](role-scope.md), [Existing Ziti resources](existing-resources.md)
- [Edge routers](routers.md), [Full control](full-control.md)
- [Expose an Ingress](ingress.md), [Sidecar tunneler](sidecar.md), [Port forward](port-forward.md)
- [Use a cert-manager CA](cert-manager.md), [Log in with a service account token](service-account-tokens.md)
- [Serve plain and TLS ports](tls.md), [Get the CA bundle](ca-bundle.md)
- [Conditions and reasons](conditions.md), [Validation](validation.md)
- [Audit a network](audit.md), [Operations](operations.md)
- [Compatibility](compatibility.md), [Interop with ziti-k8s-agent](interop-ziti-k8s-agent.md)

## API reference

- [ZitiApp](reference/ZitiApp.md), [ZitiConnection](reference/ZitiConnection.md), [ZitiIdentity](reference/ZitiIdentity.md)
- [ZitiAccessPolicy](reference/ZitiAccessPolicy.md), [ZitiRouter](reference/ZitiRouter.md), [ZitiCA](reference/ZitiCA.md)
- [ZitiJwtSigner](reference/ZitiJwtSigner.md), [ZitiSidecar](reference/ZitiSidecar.md), [ZitiPortForward](reference/ZitiPortForward.md)
- [ZitiConfig](reference/ZitiConfig.md), [ZitiService](reference/ZitiService.md), [ZitiServicePolicy](reference/ZitiServicePolicy.md)
- [ZitiEdgeRouterPolicy](reference/ZitiEdgeRouterPolicy.md), [ZitiServiceEdgeRouterPolicy](reference/ZitiServiceEdgeRouterPolicy.md), [ZitiTerminator](reference/ZitiTerminator.md)

## Decisions

- [ADR 0001: Build a new operator](adr/0001-build-or-contribute.md)
- [ADR 0002: Service account tokens as Ziti identities](adr/0002-service-account-tokens.md)
- [ADR 0003: Cluster-wide Service write access](adr/0003-service-write-access.md)

## Import status

These pages are copied from `docs/` in the repository by `sync.py`. Edit the repository, then run `sync.py`, not this page.
