#!/bin/bash
# Eisenhower Task Dashboard Startup Script
# Automatically checks/installs dependencies and remembers the last used port

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PORT_FILE="$SCRIPT_DIR/port.conf"

# Check and install dependencies if needed
if [ ! -d "$SCRIPT_DIR/node_modules" ]; then
  echo "[Dashboard] First time setup - installing dependencies..."
  bash "$SCRIPT_DIR/check-and-install.sh"
  if [ $? -ne 0 ]; then
    exit 1
  fi
fi

# Read saved port (default: 8080)
if [ -f "$PORT_FILE" ]; then
    SAVED_PORT=$(cat "$PORT_FILE" | tr -d '[:space:]')
fi
SAVED_PORT=${SAVED_PORT:-8080}

# Check if user specified a port via --port argument
USER_PORT=""
for ((i=1; i<=$#; i++)); do
    arg="${!i}"
    if [ "$arg" = "--port" ]; then
        next=$((i+1))
        if [ $next -le $# ]; then
            USER_PORT="${!next}"
        fi
        break
    fi
done

# Determine which port to use
if [ -n "$USER_PORT" ]; then
    # User specified a port, save it for next time
    echo "$USER_PORT" > "$PORT_FILE"
    echo "[Dashboard] Port saved: $USER_PORT"
else
    # No port specified, use saved port
    set -- "$@" --port "$SAVED_PORT"
    echo "[Dashboard] Using saved port: $SAVED_PORT"
fi

cd "$SCRIPT_DIR"
node server.js "$@"