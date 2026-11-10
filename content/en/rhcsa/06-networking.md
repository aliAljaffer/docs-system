# 6. Networking

**Goal:** Identify network interfaces, set the hostname, and change IP settings with `ip`.

## Interface names

Interface names come from the hardware. The classic names are `eth{0..9}`.

| Prefix | Interface type |
|--------|----------------|
| `em` | Embedded NIC |
| `eno` | Embedded NIC |
| `p<slot>p<port>` | NIC on the PCI bus |

Show the interfaces and their names:

```bash
ip link show
```

Show the IP settings of the interfaces:

```bash
ip addr show
```

The `lo` device is the loopback interface. Its addresses are `127.0.0.1` and `::1`.

## Hostname

Set the hostname:

```bash
hostnamectl set-hostname <name>
```

The command writes the hostname to `/etc/hostname`.

## Name resolution

| File | Purpose |
|------|---------|
| `/etc/hosts` | Maps IP addresses to hostnames. Format: `[ip] [hostname]` |
| `/etc/resolv.conf` | DNS client settings |
| `/etc/nsswitch.conf` | Order of name resolution. You can set DNS to resolve before `/etc/hosts`. |

## Change IP settings with ip

!!! warning "Not persistent"
    Changes made with `ip` do not survive a reboot. Use `ip`, not `ifconfig`.

Add an IP address to an interface for testing:

```bash
ip addr add dev ens33 10.0.0.10/24
```

Add a default route:

```bash
ip route add default via 10.0.0.1
```

Show routes:

```bash
ip route show
```

Show packet statistics:

```bash
ip -s link
```

## Exam tips

- Use `ip`, not `ifconfig`.
- Changes made with `ip` are not persistent.
- Know that `hostnamectl` writes to `/etc/hostname`.
- Check `/etc/nsswitch.conf` for the name resolution order.
- Read `10.0.0.10/24` as an address with a network prefix. See [[cidr]].

[Back to course overview](index.md)
