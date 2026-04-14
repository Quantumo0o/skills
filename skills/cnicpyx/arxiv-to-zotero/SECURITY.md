# Security Checklist

This skill is designed for one narrow workflow only:

**one raw arXiv query → arXiv metadata fetch → Zotero dedupe cache → Zotero import → PDF upload attempt → Link to URI fallback only on HTTP 413 → one final summary**

## External Network Access

This package may contact only:

- **arXiv Atom API** for paper discovery
- **arXiv PDF URLs** for direct PDF download with `curl`
- **Zotero Web API** for duplicate checks, item creation, PDF attachment upload, and fallback link attachment creation

## Secrets and Credentials

Expected runtime secret:

- `ZOTERO_API_KEY`

Rules:

- do not hard-code secrets into the package
- provide secrets through `~/.openclaw/.env` or the current process environment
- do not place real API keys in `config.json`
- do not print secrets in normal output or logs

## Local Files Read

The skill may read:

- the config path passed by `--config`, or the bundled `config.json` in the skill root directory
- `~/.openclaw/config/skills/arxiv-to-zotero.setup.json`
- `~/.openclaw/.env`
- bundled docs such as `setup.md`, `README.md`, and `SKILL.md`

## Local Files Written

The skill may write:

- `~/.openclaw/config/skills/arxiv-to-zotero.setup.json`
- the optional JSON run summary path configured by `run.export_summary_path`
- temporary PDF files in the system temp directory during upload attempts

## Explicit Non-Goals

- no modification of existing Zotero paper items
- no access to unrelated local files or credentials
