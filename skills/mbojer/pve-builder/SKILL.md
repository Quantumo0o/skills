---
name: pve-builder
description: >
  Generate Proxmox VE CLI commands to create a new VM. Use when asked to create a VM,
  provision a virtual machine on Proxmox, generate qm commands, set up a new VM,
  or when given a workload description and asked what Proxmox config it needs.
version: 1.0.0
tags:
  - proxmox
  - homelab
  - infrastructure
  - vm
  - devops
  - latest
metadata:
  openclaw:
    requires:
      bins:
        - pvesh
        - qm
    security_tier: L2
---

# pve-builder

Generate complete, copy-pasteable Proxmox VE 9 CLI commands to create and configure a new VM
from a plain-language workload description.

## When to use this skill

Activate when the user:
- Asks to create or provision a new VM on Proxmox
- Provides a workload description and wants `qm` commands
- Shares a URL and asks what VM it needs
- Asks for Proxmox CLI commands for any specific software or use case

---

## Workflow

Follow these steps in order. Do not skip steps or generate commands before completing them all.

### Step 1 — Read environment memory

Read `references/pve-env.md` before doing anything else.
Note all known values (node, storage, bridge, ISOs). You will use these as defaults.

### Step 2 — Understand the workload

If the user provided a URL:
- Fetch the URL and read its content
- Identify the software, its purpose, and any stated system requirements

If the page returns no useful content or the URL fails:
- Search the web for: `"<software name> system requirements recommended specs"`
- Use the search results to determine RAM, CPU, disk, and OS recommendations

If web search is unavailable:
- Ask the user: *"I can't look that up right now — can you briefly describe what this software does and roughly how demanding it is?"*
- Use the description plus your own knowledge to recommend specs

### Step 3 — Determine VM specs

Based on what you know about the workload, recommend:

| Parameter | How to decide |
|---|---|
| RAM | Match workload requirements + 20% headroom. Round to nearest power of 2 in MB. |
| CPU cores | 2 for light workloads, 4 for medium, 6–8 for heavy. |
| Disk size | Follow official recommendations if available. Add 20% buffer. |
| OS | Prefer Debian 12 for Linux daemons unless the workload specifies otherwise. |
| BIOS | SeaBIOS for Linux VMs. OVMF (UEFI) for Windows or if user requests it. |
| Machine type | `q35` for all new VMs. |
| Disk bus | `scsi` with `virtio-scsi-pci` controller. |
| Network | `virtio` driver. |

Always show your reasoning: *"For Home Assistant I'm recommending 4GB RAM based on their official docs."*
If uncertain, show two options and ask the user to choose.

### Step 4 — Resolve environment values

Check `references/pve-env.md` for each of these. For each:
- **Known** → confirm with user: *"Same as last time — `<value>`?"*
- **Unknown** → ask the user directly

Values to resolve:
- `node` — Proxmox node name (e.g. `pve`)
- `storage` — Storage pool for the VM disk (e.g. `local-lvm`, `local-zfs`)
- `bridge` — Network bridge (e.g. `vmbr0`)
- `vlan_tag` — Optional. Ask only if user mentions VLANs.
- `start_on_boot` — Ask: *"Should this VM start automatically when Proxmox boots?"*
- `start_after_create` — Ask: *"Should I include the command to start the VM immediately after creation?"*

Do **not** ask for a VM ID. This is resolved automatically in the output (see Step 5).

### Step 5 — Resolve ISO

Check `references/pve-env.md` under `## Known ISOs` for an entry matching the required OS.

- **Matching ISO found** → confirm with user: *"I have `<path>` on record for `<os>` — still valid?"*
- **No match found** →
  1. Search the web for the official cloud image or ISO download URL for the required OS
  2. Ask the user: *"Which storage location should I download it to?"* (e.g. `local`)
  3. Include a `wget` + `qm importdisk` block at the top of the output

### Step 6 — Generate commands

Only generate commands once all values from Steps 3–5 are confirmed.

Output a single fenced shell block using this structure:

```bash
# ============================================================
# pve-builder — <VM Name>
# Workload: <one-line description>
# Generated: <today's date>
# ============================================================

# STEP 1: Get next available VM ID
# Run this first. The result is used throughout the script.
VMID=$(pvesh get /cluster/nextid)
echo "Using VM ID: $VMID"

# STEP 2 (if ISO download needed): Download OS image
# wget -O /var/lib/vz/template/iso/<filename>.iso <download_url>

# STEP 3: Create VM
qm create $VMID \
  --name <vm-name> \
  --memory <mb> \
  --cores <n> \
  --cpu x86-64-v2-AES \
  --machine q35 \
  --bios <seabios|ovmf> \
  --ostype <l26|win11> \
  --scsihw virtio-scsi-pci \
  --node <node>

# STEP 4: Attach disk
qm set $VMID --scsi0 <storage>:32,format=raw,discard=on

# STEP 5: Attach ISO (or cloud image)
qm set $VMID --ide2 <storage>:iso/<filename>.iso,media=cdrom
qm set $VMID --boot order=scsi0;ide2

# STEP 6: Configure network
qm set $VMID --net0 virtio,bridge=<bridge>[,tag=<vlan>]

# STEP 7: Cloud-init (include only if using a cloud image)
qm set $VMID --ide0 <storage>:cloudinit
qm set $VMID --ipconfig0 ip=dhcp
qm set $VMID --ciuser <username> --cipassword <password>
qm cloudinit update $VMID

# STEP 8: Misc settings
qm set $VMID --onboot <1|0>
qm set $VMID --agent enabled=1
qm set $VMID --tablet 0

# STEP 9: Start VM (if requested)
# qm start $VMID
# echo "VM $VMID started. Find it in the Proxmox dashboard under: Node > $VMID"
```

**Notes to include below the block:**
- Remind the user to verify any ISO path that came from memory
- Mention where to find the VM in the Proxmox UI after creation
- If OVMF was used, note that an EFI disk is required:
  `qm set $VMID --efidisk0 <storage>:0,efitype=4m,pre-enrolled-keys=1`

### Step 7 — Update environment memory

After generating commands, update `references/pve-env.md` with any new or changed values:
- node, storage, bridge, vlan_tag (if provided)
- Any new ISO entry under `## Known ISOs`

Do not remove existing entries. Add or overwrite only what changed.

---

## Constraints

- **Never generate commands before resolving all unknowns.** Partial commands cause broken VMs.
- **Never invent storage pool or bridge names.** Always ask if not in memory.
- **Never skip Step 1** (read `references/pve-env.md`).
- **Never skip Step 7** (write back to `references/pve-env.md`).
- **Do not include `qm start` as a regular step** — always wrap it in a comment and only uncomment if the user confirmed they want immediate start.
- **Do not guess VM ID.** Always use `pvesh get /cluster/nextid` via the shell variable pattern.
- If the user provides requirements that seem unusually low (e.g. 512MB RAM for a modern Linux daemon), flag it: *"That's below what I'd recommend — want to proceed anyway?"*

---

## References

- `references/pve-env.md` — Persistent environment config. Read on start, write on finish.
- `references/qm-reference.md` — `qm` flag cheatsheet for Proxmox 9. Load when you need to verify a flag name or option.
