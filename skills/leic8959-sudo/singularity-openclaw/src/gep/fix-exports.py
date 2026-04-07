import os, re

def fix_module(fname):
    fpath = os.path.join('.', fname)
    with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    fns = re.findall(r'(?:async )?function (\w+)', content)
    if not fns:
        print('No functions found in:', fname)
        return

    # Remove all export keywords
    content = re.sub(r'^export async function ', 'async function ', content, flags=re.MULTILINE)
    content = re.sub(r'^export function ', 'function ', content, flags=re.MULTILINE)
    content = re.sub(r'^export const ', 'const ', content, flags=re.MULTILINE)

    # Build named exports line
    exports_line = ', '.join(sorted(set(fns)))

    # Append module.exports
    content = content.rstrip() + '\n\nmodule.exports = { ' + exports_line + ' };\n'

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Fixed:', fname, '-> exports:', len(fns), 'functions')

for fname in ['assetStore.cjs', 'capsuleRecorder.cjs', 'canary.cjs']:
    fix_module(fname)
