#!/bin/bash
# bootleg-ssh.sh - SSH through alternative methods

set -e

usage() {
    echo "Bootleg SSH - Alternative SSH connection methods"
    echo "Usage: $0 [method] [options]"
    echo ""
    echo "Methods:"
    echo "  http-proxy    - SSH through HTTP CONNECT proxy"
    echo "  websocket     - SSH through WebSocket tunnel"
    echo "  port-443      - SSH on port 443 (HTTPS)"
    echo "  dns-tunnel    - SSH through DNS tunnel (requires iodine)"
    echo ""
    echo "Examples:"
    echo "  $0 http-proxy --proxy proxy.example.com:8080 user@server"
    echo "  $0 port-443 user@server.example.com"
    exit 1
}

method_http_proxy() {
    local proxy="$1"
    local target="$2"
    
    if [ -z "$proxy" ] || [ -z "$target" ]; then
        echo "Error: Missing proxy or target"
        usage
    fi
    
    echo "Connecting via HTTP proxy: $proxy"
    ssh -o ProxyCommand="nc -X connect -x $proxy %h %p" "$target"
}

method_websocket() {
    local ws_url="$1"
    local target="$2"
    
    if [ -z "$ws_url" ] || [ -z "$target" ]; then
        echo "Error: Missing WebSocket URL or target"
        usage
    fi
    
    echo "Connecting via WebSocket: $ws_url"
    # This requires websocat to be installed
    if ! command -v websocat &> /dev/null; then
        echo "Error: websocat not installed. Install with: cargo install websocat"
        exit 1
    fi
    
    # Extract host and port from target
    local host=$(echo "$target" | cut -d@ -f2 | cut -d: -f1)
    local port=$(echo "$target" | cut -d: -f2)
    port=${port:-22}
    
    echo "Creating WebSocket to TCP bridge..."
    websocat "$ws_url" "tcp:$host:$port"
}

method_port_443() {
    local target="$1"
    
    if [ -z "$target" ]; then
        echo "Error: Missing target"
        usage
    fi
    
    echo "Connecting on port 443 (HTTPS)"
    ssh -p 443 "$target"
}

method_dns_tunnel() {
    local dns_server="$1"
    
    if [ -z "$dns_server" ]; then
        echo "Error: Missing DNS server"
        usage
    fi
    
    echo "Setting up DNS tunnel to $dns_server"
    echo "Note: This requires iodine server setup on the remote side"
    
    if ! command -v iodine &> /dev/null; then
        echo "Error: iodine not installed. Install with: sudo apt-get install iodine"
        exit 1
    fi
    
    # Start iodine client
    sudo iodine -f -r "$dns_server"
    
    echo "Once connected, SSH to 10.0.0.1"
    echo "ssh user@10.0.0.1"
}

# Main script
if [ $# -lt 1 ]; then
    usage
fi

METHOD="$1"
shift

case "$METHOD" in
    http-proxy)
        method_http_proxy "$@"
        ;;
    websocket)
        method_websocket "$@"
        ;;
    port-443)
        method_port_443 "$@"
        ;;
    dns-tunnel)
        method_dns_tunnel "$@"
        ;;
    *)
        echo "Error: Unknown method: $METHOD"
        usage
        ;;
esac