import argparse
import urllib.request
import urllib.error
import urllib.parse
import json
import os
import sys

def main():
    parser = argparse.ArgumentParser(description="Trigger the eonik Meta Ads audit")
    parser.add_argument("--account_id", required=True, help="Meta Ad Account ID (e.g., act_12345)")
    parser.add_argument("--days", type=int, default=7, help="Days to evaluate (default: 7)")
    args = parser.parse_args()

    api_key = os.environ.get("EONIK_API_KEY")
    if not api_key:
        print(json.dumps({
            "status": "error",
            "message": "EONIK_API_KEY environment variable is not set."
        }, indent=2), file=sys.stderr)
        sys.exit(1)
        
    # Security: Drop the ephemeral key from the execution environment securely.
    del os.environ["EONIK_API_KEY"]

    # The Endpoint Requirements
    endpoint = "https://api.eonik.ai/api/budget-agent/run-audit"
    
    headers = {
        "x-api-key": api_key,
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    params = {
        "account_id": args.account_id,
        "days": args.days
    }

    try:
        query_string = urllib.parse.urlencode(params)
        full_url = f"{endpoint}?{query_string}"
        
        req = urllib.request.Request(full_url, headers=headers, method="POST")
        
        with urllib.request.urlopen(req) as response:
            body = response.read().decode('utf-8')
            report = json.loads(body)
        
        # Output the full report to pass to the notification stage
        print(json.dumps({
            "status": "success",
            "flagged_ads_count": report.get("flagged_ads_count", 0),
            "total_leaked_spend": report.get("total_leaked_spend", 0.0),
            "pause_recommendations": report.get("pause_recommendations", []),
            "scale_recommendations": report.get("scale_recommendations", []),
            "monitor_recommendations": report.get("monitor_recommendations", [])
        }, indent=2))
        
    except urllib.error.HTTPError as http_err:
        err_body = http_err.read().decode('utf-8')
        print(json.dumps({
            "status": "error",
            "message": f"HTTP error occurred: {http_err.code} {http_err.reason}",
            "response_text": err_body
        }, indent=2), file=sys.stderr)
        sys.exit(1)
    except Exception as err:
        print(json.dumps({
            "status": "error",
            "message": f"An unexpected error occurred: {err}"
        }, indent=2), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
