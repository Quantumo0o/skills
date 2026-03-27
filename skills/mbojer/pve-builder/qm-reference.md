# qm Reference — Proxmox VE 9

Quick reference for the agent. Load this file when verifying flag names, values, or syntax.

---

## Core create flags (`qm create`)

| Flag | Type | Notes |
|---|---|---|
| `--name` | string | VM display name |
| `--memory` | int (MB) | RAM in megabytes (e.g. `4096`) |
| `--cores` | int | vCPU count |
| `--sockets` | int | CPU socket count (default `1`) |
| `--cpu` | string | CPU type. Use `x86-64-v2-AES` for modern Linux, `host` for passthrough |
| `--machine` | string | `q35` (recommended) or `i440fx` (legacy) |
| `--bios` | string | `seabios` (default) or `ovmf` (UEFI) |
| `--ostype` | string | See OS types below |
| `--scsihw` | string | `virtio-scsi-pci` (recommended) or `lsi` (legacy) |
| `--node` | string | Proxmox node name |

---

## OS types (`--ostype`)

| Value | Use for |
|---|---|
| `l26` | Linux kernel 2.6+ (Debian, Ubuntu, etc.) |
| `l24` | Linux kernel 2.4 (very old) |
| `win11` | Windows 11 |
| `win10` | Windows 10 / Server 2016–2022 |
| `win8` | Windows 8 / Server 2012 |
| `other` | Any other OS |

---

## Disk flags (`qm set --scsiN`)

```
qm set <vmid> --scsi0 <storage>:<size>,format=<fmt>,discard=on,ssd=1
```

| Option | Values | Notes |
|---|---|---|
| `format` | `raw`, `qcow2` | Use `raw` for LVM/ZFS, `qcow2` for dir-based storage |
| `discard` | `on` / `off` | Enable TRIM passthrough |
| `ssd` | `1` / `0` | Emulate SSD — cosmetic for guest OS |
| `cache` | `none`, `writeback` | Use `none` for ZFS; `writeback` for others |

To import an existing image as a disk:
```bash
qm importdisk <vmid> <image-path> <storage>
# Then attach it:
qm set <vmid> --scsi0 <storage>:vm-<vmid>-disk-0
```

---

## CD-ROM / ISO flags

```bash
# Attach ISO as CD-ROM
qm set <vmid> --ide2 <storage>:iso/<filename>.iso,media=cdrom

# Set boot order (disk first, then cdrom)
qm set <vmid> --boot order=scsi0;ide2

# Remove CD-ROM after install
qm set <vmid> --ide2 none,media=cdrom
```

---

## Network flags (`qm set --netN`)

```
qm set <vmid> --net0 virtio,bridge=<bridge>[,tag=<vlan>][,firewall=1]
```

| Option | Notes |
|---|---|
| `virtio` | Recommended driver for Linux guests |
| `e1000` | Use for Windows guests without VirtIO drivers loaded |
| `bridge` | The Linux bridge on the host (e.g. `vmbr0`) |
| `tag` | VLAN tag (optional) |
| `firewall` | `1` to enable Proxmox firewall on this NIC |

---

## Cloud-init flags

```bash
qm set <vmid> --ide0 <storage>:cloudinit        # Attach cloud-init drive
qm set <vmid> --ipconfig0 ip=dhcp               # DHCP on first NIC
qm set <vmid> --ipconfig0 ip=<cidr>,gw=<gw>     # Static IP
qm set <vmid> --ciuser <username>
qm set <vmid> --cipassword <password>
qm set <vmid> --sshkeys ~/.ssh/authorized_keys
qm cloudinit update <vmid>                       # Apply changes
```

Cloud-init requires a cloud image (not a standard ISO). Common images:
- Debian: `https://cloud.debian.org/images/cloud/bookworm/latest/debian-12-generic-amd64.qcow2`
- Ubuntu: `https://cloud-images.ubuntu.com/jammy/current/jammy-server-cloudimg-amd64.img`

---

## UEFI / EFI disk (required when `--bios ovmf`)

```bash
qm set <vmid> --efidisk0 <storage>:0,efitype=4m,pre-enrolled-keys=1
```

Omit `pre-enrolled-keys=1` if using Linux (Secure Boot not needed).

---

## Misc useful flags

| Flag | Notes |
|---|---|
| `--onboot 1` | Start VM on Proxmox host boot |
| `--agent enabled=1` | Enable QEMU Guest Agent (install `qemu-guest-agent` in guest) |
| `--tablet 0` | Disable USB tablet (saves CPU for headless VMs) |
| `--balloon 0` | Disable memory ballooning (for VMs with static RAM) |
| `--numa 1` | Enable NUMA (for VMs with many cores) |
| `--protection 1` | Prevent accidental deletion |
| `--description "..."` | Add a note visible in the Proxmox UI |

---

## Post-create lifecycle commands

```bash
qm start <vmid>           # Start the VM
qm stop <vmid>            # Immediately stop (like pulling power)
qm shutdown <vmid>        # Graceful shutdown via guest agent
qm status <vmid>          # Check running state
qm destroy <vmid>         # Delete VM and its disks
qm clone <vmid> <newid>   # Clone a VM
qm snapshot <vmid> <name> # Create a snapshot
```

---

## Get next available VM ID (cluster-aware)

```bash
VMID=$(pvesh get /cluster/nextid)
```

Always use this instead of picking an ID manually — it checks all nodes in the cluster.
