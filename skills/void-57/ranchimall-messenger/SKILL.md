---
name: messenger_send_node
description: Use this skill whenever you are asked to send a message using the FLO blockchain. This is the primary way to send FLO messages programmatically.
requires:
  binaries:
    - node
  env:
    - FLO_PRIVATE_KEY
---

# Messenger Send Node Skill

When the user asks to send a message, you must use your command execution tool (e.g., `exec` or `run_command`) to run the `send_node.js` script.

## Setup & Dependencies
The `ws` dependency is required and is assumed to be installed.

## Network Activity Warning
**Note**: At runtime, this script fetches a supernode list from the FLO blockchain and establishes wss/https connections to discovered supernodes to broadcast the transaction. Network activity is expected and required for the application to function.

## Security & Credentials
- The script strictly requires the `FLO_PRIVATE_KEY` environment variable.
- You should verify that `FLO_PRIVATE_KEY` is present in the environment before execution.
- If the user provides a new or different private key during the conversation, you MUST temporarily set or update the `FLO_PRIVATE_KEY` environment variable for the script execution context (e.g., `$env:FLO_PRIVATE_KEY="<new_key>"; node send_node.js ...`).
- Never prompt the user to paste their private key in the chat if they already have one present in the environment.

## Execution
Immediately execute the script using the arguments provided by the user. Ensure you format the command exactly like this:

```powershell
node send_node.js --receiver "<RECEIVER_FLO_ID>" --message "<MESSAGE>"
```