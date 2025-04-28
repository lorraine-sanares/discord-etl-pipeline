"""
Discord ETL Pipeline

1. Export guild structure
2. Export chat histories
3. JSON → CSV (csv_files)

Run:
  $ uv run discord_etl_pipeline.py
"""

import glob
import os
import pandas as pd
import json
import subprocess
from dotenv import load_dotenv

# Ensure directories
os.makedirs("csv_files", exist_ok=True)


def run_step(script):
    print(f"▶️ {script}…")
    subprocess.run(["uv", "run", script], check=True)


def export_chat_history(json_file, csv_file):
    with open(os.path.join("json_files", json_file), "r", encoding="utf-8") as f:
        msgs = json.load(f)
    df = pd.DataFrame(msgs)
    if "created_at" not in df:
        print(f"❌ {json_file} missing timestamps, skipping.")
        return
    df["created_at"] = pd.to_datetime(df["created_at"], utc=True, errors="coerce")
    df = df.dropna(subset=["created_at"]).set_index("created_at")
    df.to_csv(os.path.join("csv_files", csv_file))
    print(f"✅ {csv_file}: {len(df)} rows")


def main():
    load_dotenv()
    run_step("discord_guild_channel_exporter.py")
    run_step("discord_chat_history_exporter.py")

    for path in glob.glob("json_files/*_history.json"):
        base = os.path.basename(path).rsplit(".json", 1)[0]
        export_chat_history(f"{base}.json", f"{base}_chat_history.csv")

if __name__ == "__main__":
    main()