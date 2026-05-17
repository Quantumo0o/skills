# IMM-Romania - Verification Notes

**Last refreshed:** 2026-04-13
**Version:** 0.4.0

---

## Ce este verificat aici

Acest document a fost aliniat la suprafața CLI curentă a repo-ului și la documentația principală.

În mod explicit, această actualizare confirmă:
- comanda principală `imm-romania`
- modulele disponibile: `mail`, `cal`, `calendar`, `tasks`, `analytics`, `sync`, `files`
- subcomenzile expuse de help-ul curent
- faptul că task-urile folosesc `trash`, nu `delete`

Pentru verificare funcțională live împotriva Exchange / Nextcloud, rulează checklist-ul de smoke test de mai jos.

---

## ✅ Command Reference (current CLI surface)

### Mail Commands

```bash
imm-romania mail connect
imm-romania mail read --limit 10
imm-romania mail read --unread
imm-romania mail get --id ID
imm-romania mail send --to EMAIL --subject SUBJECT --body BODY
imm-romania mail draft --to EMAIL --subject SUBJECT --body BODY
imm-romania mail reply --id ID --body BODY
imm-romania mail forward --id ID --to EMAIL
imm-romania mail mark --id ID --read
imm-romania mail mark --id ID --unread
imm-romania mail mark-all-read
imm-romania mail list-attachments --id ID
imm-romania mail download-attachment --id ID --name FILE --output DIR
```

### Calendar Commands

```bash
imm-romania cal connect
imm-romania cal list --days 7
imm-romania cal today
imm-romania cal week
imm-romania cal get --id ID
imm-romania cal create --subject SUBJECT --start DATETIME [--duration MIN]
imm-romania cal update --id ID
imm-romania cal delete --id ID
imm-romania cal respond --id ID
imm-romania cal availability
```

Aliasul `calendar` este de asemenea acceptat de entrypoint-ul unificat.

### Tasks Commands

```bash
imm-romania tasks connect
imm-romania tasks list
imm-romania tasks list --overdue
imm-romania tasks list --status STATUS
imm-romania tasks get --id ID
imm-romania tasks create --subject SUBJECT [--due DATE] [--priority LEVEL]
imm-romania tasks assign --to EMAIL --subject SUBJECT [--body BODY] [--due DATE]
imm-romania tasks update --id ID
imm-romania tasks complete --id ID
imm-romania tasks trash --id ID
```

### Analytics Commands

```bash
imm-romania analytics stats --days N
imm-romania analytics response-time
imm-romania analytics top-senders
imm-romania analytics heatmap
imm-romania analytics folders
imm-romania analytics report
```

### Sync Commands

```bash
imm-romania sync sync
imm-romania sync reminders [--hours N] [--dry-run]
imm-romania sync link-calendar --id TASK_ID [--time HH:MM] [--duration MIN]
imm-romania sync status
```

### Files Commands (Nextcloud)

```bash
imm-romania files list [PATH] [--recursive]
imm-romania files search QUERY [PATH]
imm-romania files extract-text PATH
imm-romania files summarize PATH
imm-romania files ask-file PATH QUESTION
imm-romania files extract-actions PATH
imm-romania files create-tasks-from-file PATH [--mailbox EMAIL] [--priority LEVEL] [--select 1,2] [--execute]
imm-romania files upload LOCAL REMOTE
imm-romania files download REMOTE LOCAL
imm-romania files mkdir PATH
imm-romania files delete PATH
imm-romania files move OLD NEW
imm-romania files copy SRC DEST
imm-romania files info PATH
imm-romania files shared
imm-romania files share-create PATH [--password VALUE] [--expire-date YYYY-MM-DD] [--public-upload]
imm-romania files share-list [PATH]
imm-romania files share-revoke SHARE_ID
```

---

## 🔎 Accuracy Notes

### Task deletion semantics

Pentru Exchange tasks, comanda documentată corect este:

```bash
imm-romania tasks trash --id TASK_ID
```

Asta mută task-ul în **Deleted Items** și este varianta sigură / recuperabilă.

### File-to-task workflow semantics

`create-tasks-from-file` este documentată ca workflow **preview-first**:
- fără `--execute` → vezi propunerile
- cu `--select ... --execute` → creezi efectiv task-urile selectate

### Mail commands

Comanda `draft-reply` **nu** este în suprafața CLI curentă. Documentația trebuie să folosească doar comenzile expuse mai sus.

---

## 🧪 Smoke Test Checklist

Rulează înainte de release sau demo live:

```bash
# Exchange
imm-romania mail connect
imm-romania mail read --limit 5
imm-romania cal today
imm-romania tasks list
imm-romania analytics stats --days 7
imm-romania sync status

# Nextcloud
imm-romania files list /
imm-romania files search contract /Clients/
imm-romania files extract-text /Clients/contract.docx
imm-romania files summarize /Clients/contract.docx
imm-romania files ask-file /Clients/contract.docx "When is the renewal due?"
imm-romania files extract-actions /Clients/contract.txt
imm-romania files create-tasks-from-file /Clients/contract.txt
imm-romania files share-list
imm-romania files shared
```

---

## 📝 Known Documentation Decisions

- top-level docs optimizează pentru CLI-ul unificat `imm-romania ...`
- documentația de setup evită exemplele vechi de tip `python3 -m modules.exchange ...`
- pentru task-uri, limbajul preferat este **trash / move to Deleted Items**, nu delete dur

---

## 📚 Related Docs

- `README.md` — overview și quickstart
- `SKILL.md` — descrierea skill-ului pentru OpenClaw
- `references/setup.md` — instalare și configurare
- `CHANGELOG.md` — istoric versiuni
