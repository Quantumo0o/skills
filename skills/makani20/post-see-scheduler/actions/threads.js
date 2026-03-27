#!/usr/bin/env node
'use strict';
const { createPlatformApi, runCli } = require('./post-see-client');
const PLATFORM = 'threads';
module.exports = createPlatformApi(PLATFORM);
if (require.main === module) runCli(PLATFORM);
