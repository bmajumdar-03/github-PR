import json
import os
import sys


def main():
    payload_file = "orchestrator_feedback.json"

    if not os.path.exists(payload_file):
        print(f"Error: {payload_file} not found. Mock Orchestrator cannot execute.")
        sys.exit(1)

    print("\n" + "=" * 50)
    print("🤖 MAIN ORCHESTRATION AGENT (SIMULATED) ACTIVATED")
    print("=" * 50)

    with open(payload_file, "r") as f:
        payload = json.load(f)

    print(f"► Received Source  : {payload.get('feedback_source')}")
    print(f"► Target File      : {payload.get('target_file')}")
    print(f"► Active Branch    : {payload.get('branch')}")
    print(f"► Feedback Comment : \"{payload.get('error_context')}\"")
    print("-" * 50)
    print("► CURRENT FAILING CODE:")
    print(payload.get("failed_code"))
    print("-" * 50)

    # This is where your AI generation code will eventually reside.
    # We will simulate a generated fix to prove the loop is functional:
    print("🔧 Simulated Action: Rewriting target_query.sql to correct syntax error...")

    corrected_sql = (
        "-- Converted SQL Query (Auto-Corrected based on PR feedback)\n"
        "SELECT id, name, date_created \n"
        "FROM my_table \n"
        "WHERE id = 1; -- Applied syntax optimization comment"
    )

    # Overwrite the local file with the simulated fix
    local_file_path = payload.get("target_file")
    with open(local_file_path, "w") as f:
        f.write(corrected_sql)

    print(f"✅ Success: Converted query updated locally in '{local_file_path}'.")
    print("💡 Next Step: Run test_git_flow.py to commit and push the correction!")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    main()
