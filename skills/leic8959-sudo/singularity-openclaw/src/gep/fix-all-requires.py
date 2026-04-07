import re, os

# Fix all .js require paths to .cjs in gep .cjs files
GEP = r'C:\Users\29248\Desktop\singularity\src\gep'

files = [
    'sessionReader.cjs','idleScheduler.cjs','paths.cjs','config.cjs',
    'gitOps.cjs','policyCheck.cjs','solidify.cjs','llmReview.cjs',
    'assetStore.cjs','hubSearch.cjs','capsuleRecorder.cjs',
    'signalMatcher.cjs','ingestGene.cjs',
]

for fname in files:
    fpath = os.path.join(GEP, fname)
    with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
        c = f.read()
    original = c

    # Replace all require('./X.js') with require('./X.cjs')
    c = c.replace("require('./assetStore.js')", "require('./assetStore.cjs')")
    c = c.replace("require('./capsuleRecorder.js')", "require('./capsuleRecorder.cjs')")
    c = c.replace("require('./hubSearch.js')", "require('./hubSearch.cjs')")
    c = c.replace("require('./signalMatcher.js')", "require('./signalMatcher.cjs')")
    c = c.replace("require('./ingestGene.js')", "require('./ingestGene.cjs')")
    c = c.replace("require('./idleScheduler.js')", "require('./idleScheduler.cjs')")
    c = c.replace("require('./sessionReader.js')", "require('./sessionReader.cjs')")
    c = c.replace("require('./paths.js')", "require('./paths.cjs')")
    c = c.replace("require('./config.js')", "require('./config.cjs')")
    c = c.replace("require('./gitOps.js')", "require('./gitOps.cjs')")
    c = c.replace("require('./policyCheck.js')", "require('./policyCheck.cjs')")
    c = c.replace("require('./solidify.js')", "require('./solidify.cjs')")
    c = c.replace("require('./llmReview.js')", "require('./llmReview.cjs')")
    # Fix ../lib/api.js
    c = c.replace("require('../lib/api.js')", "require('../lib/api.js')")  # already .js, keep as is
    # Also fix without explicit extension
    c = re.sub(r"require\('\./(\w+)\.js'\)", lambda m: "require('./" + m.group(1) + ".cjs')", c)

    if c != original:
        print('Fixed:', fname)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(c)
    else:
        print('OK:', fname)
