import argparse
import subprocess
import json
import sys
import os
import datetime

def run_command(cmd, env=None):
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True, env=env)
    if result.returncode != 0:
        print(f"Error executing command: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    return result.stdout

def main():
    parser = argparse.ArgumentParser(description="Run Meta Ads Audit Pipeline")
    parser.add_argument("--config", required=True, help="Path to config.json")
    args = parser.parse_args()

    # Load config to get account_id and days
    try:
        with open(args.config, 'r') as f:
            config = json.load(f)
    except Exception as e:
        print(f"Failed to load config: {e}", file=sys.stderr)
        sys.exit(1)

    account_id = config.get("meta", {}).get("account_id")
    days = config.get("meta", {}).get("evaluation_days", 7)
    
    if not account_id:
        print("meta.account_id is required in config", file=sys.stderr)
        sys.exit(1)

    run_date = datetime.datetime.now().strftime("%Y-%m-%d")
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    report_path = os.path.join(output_dir, f"audit-{run_date}.json")

    # Step 1: Run Audit
    print("=== Stage 1: Running Audit ===")
    audit_cmd = [
        sys.executable, "scripts/audit.py",
        "--account_id", account_id,
        "--days", str(days)
    ]
    # Keep current environment so EONIK_API_KEY passes through
    audit_out = run_command(audit_cmd, env=os.environ.copy())
    
    with open(report_path, "w") as f:
        f.write(audit_out)
    
    print(f"Audit complete. Report saved to {report_path}")

    # Step 2: Dispatch Notifications
    print("\n=== Stage 2: Dispatching Notifications ===")
    notify_cmd = [
        sys.executable, "scripts/notify.py",
        "--config", args.config,
        "--report", report_path
    ]
    notify_out = run_command(notify_cmd)
    print(notify_out)
    print("Pipeline Complete!")

if __name__ == "__main__":
    main()
