#!/usr/bin/env node
/** X (Twitter) — API platform slug is `x` (not `twitter`). */
'use strict';
const { createPlatformApi, runCli } = require('./post-see-client');
const PLATFORM = 'x';
module.exports = createPlatformApi(PLATFORM);
if (require.main === module) runCli(PLATFORM);
