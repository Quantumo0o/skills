# Proxmox Environment
# ---------------------------------------------------------------
# pve-builder reads this file at the start of every session and
# writes updated values back when done.
#
# Fill in your values below. Leave a field blank if unknown —
# the agent will ask and fill it in for you.
# ---------------------------------------------------------------

node:
storage:
bridge:
vlan_tag:

## Known ISOs
# Format: - <os-label>: <storage>:iso/<filename>
# Example: - debian-12-amd64: local:iso/debian-12.9.0-amd64-netinst.iso
#
# The agent will add entries here automatically when you download
# or confirm an ISO. You can also add them manually.
