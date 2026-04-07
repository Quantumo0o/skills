import re, os

for fname in ['policyCheck.cjs', 'solidify.cjs', 'llmReview.cjs']:
    fpath = os.path.join('.', fname)
    with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
        c = f.read()
    original = c
    # Fix bare requires without extension
    c = re.sub(r"require\('\./gitOps'\)", "require('./gitOps.cjs')", c)
    c = re.sub(r"require\('\./policyCheck'\)", "require('./policyCheck.cjs')", c)
    c = re.sub(r"require\('\./config'\)", "require('./config.cjs')", c)
    c = re.sub(r"require\('\./paths'\)", "require('./paths.cjs')", c)
    c = re.sub(r"require\('\./solidify'\)", "require('./solidify.cjs')", c)
    if c != original:
        print('Fixed:', fname)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(c)
    else:
        print('OK:', fname)
