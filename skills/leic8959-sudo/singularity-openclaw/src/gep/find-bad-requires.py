import os, re

files = [
    'sessionReader.cjs','idleScheduler.cjs','paths.cjs','config.cjs',
    'gitOps.cjs','policyCheck.cjs','solidify.cjs','llmReview.cjs',
    'assetStore.cjs','hubSearch.cjs','capsuleRecorder.cjs',
    'signalMatcher.cjs','ingestGene.cjs',
]
for fname in files:
    with open(fname, 'r', encoding='utf-8', errors='replace') as f:
        c = f.read()
    requires = re.findall(r"require\('\./[^']+'", c)
    if requires:
        print(fname, '->', requires[:5])
    else:
        print(fname, 'OK')
