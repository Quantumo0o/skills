#!/usr/bin/env node
/**
 * OpenClaw Facebook Posting Skill
 * 
 * This is the main entry point for the Facebook posting skill.
 * Commands are executed via the CLI subcommands.
 * 
 * Usage:
 *   openclaw fb-post-setup <page_id> <access_token> [page_name]
 *   openclaw fb-post-test
 *   openclaw fb-post "<message>"
 *   openclaw fb-post-image "<caption>" "<url>"
 *   openclaw fb-post-schedule "<message>" "<time>"
 *   openclaw fb-post-schedule-list
 *   openclaw fb-post-schedule-delete <post_id>
 *   openclaw fb-post-drafts
 *   openclaw fb-post-delete <post_id>
 *   openclaw fb-post-setup-help
 */

const { Command } = require('commander');
const path = require('path');
const fs = require('fs');

const program = new Command();

// Get skill directory
const skillDir = __dirname;
const commandsDir = path.join(skillDir, 'commands');

// List available commands
const commandFiles = fs.readdirSync(commandsDir).filter(f => f.endsWith('.js'));

// Register each command as a subcommand
commandFiles.forEach(file => {
  const commandName = file.replace('.js', '');
  const commandPath = path.join(commandsDir, file);
  
  // Dynamically load each command
  program.command(commandName)
    .description(`Facebook posting command: ${commandName}`)
    .action(() => {
      // Execute the command file
      require(commandPath);
    });
});

program
  .name('openclaw-facebook-posting')
  .description('Facebook Page posting for OpenClaw')
  .version('1.0.0');

program.parse();
