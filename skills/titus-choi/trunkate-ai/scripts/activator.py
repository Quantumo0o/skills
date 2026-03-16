#!/usr/bin/env python3
import os
import sys

# Correcting the path for internal imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from trunkate import optimize_prompt

def run():
    """
    Evaluates context threshold and triggers semantic pruning via Trunkate API.
    Emits the OPENCLAW_ACTION to update agent memory state.
    """
    # 1. Retrieve OpenClaw environment variables
    try:
        current_tokens = int(os.environ.get("OPENCLAW_CURRENT_TOKENS", 0))
        token_limit = int(os.environ.get("OPENCLAW_TOKEN_LIMIT", 128000))
        history_path = os.environ.get("OPENCLAW_HISTORY_PATH")
    except ValueError:
        print("Trunkate Alert: Malformed token environment variables.", file=sys.stderr)
        return

    # 2. Configuration: Proactive "Smart Buffer"
    # Default to 20% of the current history to maintain extreme density.
    target_budget = os.environ.get("TRUNKATE_AUTO_BUDGET", "20%")
    
    # Proactive Principle: We systematically optimize every call to ensure 
    # the agent's memory is always lean and cost-effective.
    if not history_path or not os.path.exists(history_path):
        return

    try:
        # 3. Read session history with safety check
        file_size = os.path.getsize(history_path)
        if file_size > 10 * 1024 * 1024:  # 10MB limit
            print(f"Trunkate Alert: History file too large ({file_size} bytes). Skipping optimization.", file=sys.stderr)
            return

        with open(history_path, "r") as f:
            history = f.read()
            
        # 4. Invoke Semantic Pruner
        optimized = optimize_prompt(history, budget=target_budget)
        
        # 5. Emit state update directive
        if optimized and optimized != history:
            print(f"OPENCLAW_ACTION:SET_HISTORY={optimized}")
            # Log success to stderr to keep stdout clean for action parsing
            print(f"Trunkate: Proactive optimization complete. Target: {target_budget}.", file=sys.stderr)
        
    except Exception as e:
        print(f"Trunkate Error: Failed to activate optimization: {e}", file=sys.stderr)

if __name__ == "__main__":
    run()