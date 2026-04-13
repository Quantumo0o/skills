#!/usr/bin/env python3
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = ROOT.name
INCLUDE_NAMES = [
    'SKILL.md',
    'appendix-auth.md',
    'requirements.txt',
    'run_campaign.py',
    'run_campaign_cycle.py',
    'wotohub_skill.py',
    'prompts',
    'references',
    'scripts',
    'steps',
]
EXCLUDE_DIR_NAMES = {'__pycache__', 'state'}
EXCLUDE_FILE_NAMES = {'.DS_Store'}
EXCLUDE_RELATIVE_PATHS = {
    Path('references/upper-layer-refactor-notes.md'),
    Path('references/model-analysis-test-cases.md'),
    Path('scripts/test_upper_layer_routing.py'),
    Path('scripts/package_skill.py'),
}


def copy_tree(src: Path, dst: Path) -> None:
    for path in src.rglob('*'):
        rel = path.relative_to(src)
        root_rel = path.relative_to(ROOT)
        if any(part in EXCLUDE_DIR_NAMES for part in rel.parts):
            continue
        if path.name in EXCLUDE_FILE_NAMES:
            continue
        if root_rel in EXCLUDE_RELATIVE_PATHS:
            continue
        target = dst / rel
        if path.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)


def main() -> int:
    output_dir = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT.parent.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix=f'{SKILL_NAME}-package-') as tmp:
        stage_root = Path(tmp) / SKILL_NAME
        stage_root.mkdir(parents=True, exist_ok=True)

        for name in INCLUDE_NAMES:
            src = ROOT / name
            if not src.exists():
                continue
            dst = stage_root / name
            if src.is_dir():
                dst.mkdir(parents=True, exist_ok=True)
                copy_tree(src, dst)
            else:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)

        cmd = [
            sys.executable,
            '/opt/homebrew/lib/node_modules/openclaw/skills/skill-creator/scripts/package_skill.py',
            str(stage_root),
            str(output_dir),
        ]
        result = subprocess.run(cmd, check=False)
        return int(result.returncode)


if __name__ == '__main__':
    raise SystemExit(main())
