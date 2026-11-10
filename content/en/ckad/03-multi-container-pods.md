# 3. Multi-container pods

Goal: Run helper containers before the main container and beside it.

## Init containers

- An init container runs before the main container.
- The main container starts only after each init container succeeds.
- An init container stops after it finishes.

## Sidecar containers

- A sidecar is an init container with `restartPolicy: Always`.
- A sidecar keeps running. It does not stop like an init container.

## Exam tips

- Know the difference: an init container stops, and a sidecar keeps running.
- Remember that the main container waits for every init container to succeed.
- Set `restartPolicy: Always` to make an init container a sidecar.

[Next: Labels and deployments](04-labels-and-deployments.md)
