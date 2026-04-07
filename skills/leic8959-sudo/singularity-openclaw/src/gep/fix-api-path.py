import re

files = ['hubSearch.cjs', 'ingestGene.cjs']
for fname in files:
    with open(fname, 'r', encoding='utf-8', errors='replace') as f:
        c = f.read()
    original = c
    c = c.replace("../lib/api.js", "../../lib/api.js")
    c = c.replace("../lib/api.cjs", "../../lib/api.cjs")
    if c != original:
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(c)
        print('Fixed path in:', fname)
    else:
        print('OK:', fname)
