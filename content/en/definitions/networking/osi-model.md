---
title: OSI Model
category: Networking
description: 'Networking note: OSI Model.'
tags:
- networking
- osi
---

<!-- imported from ObsidianVault/studies/networking/OSI Model.md. Edit the source, then run sync.py. -->

# OSI Model

`networking` `osi`

- **Physical Layer**: This is the hardware part of communication, like cables, switches, and electrical signals. It sends raw bits over the physical medium.
	- Cables, fiber, signal
- **Data Link Layer**: Ensures that data is transferred error-free over the physical link. It also handles addressing on a local network (MAC addresses).
	- The switching layer
	- Ethernet frame, mac addresses, switches, Extended Unique Identifier EUI
- **Network Layer**: Responsible for routing data between devices on different networks. It uses IP addresses to decide the best path for data to travel.
	- The "routing" layer
	- Fragments frames to traverse different networks
	- IP Address, Router, Packet
- **Transport Layer**: Ensures data is transferred reliably between devices. It handles things like error checking, flow control, and data segmentation. Common protocols here are TCP and UDP.
	- The "post office" layer
	- TCP and UDP
	- TCP Segment, UDP Datagram, ports
- **Session Layer**: Manages the opening, closing, and managing of communication sessions between devices. It keeps track of who is communicating and when.
	- Control and tunneling protocols
- **Presentation Layer**: Translates data into a format that the application layer can understand. It also handles encryption and compression.
	- SSL/TLS encryption
- **Application Layer**: This is the closest layer to the user. It's where network services like web browsing (HTTP), email (SMTP), and file transfer (FTP) operate.
	- YOUR EYES!
