"""
Discord ETL Pipeline

1. Export guild structure
2. Export all chat histories to a single CSV file

Run:
  $ uv run discord_etl_pipeline.py
"""

import os
import subprocess
from dotenv import load_dotenv

# Ensure directories
os.makedirs("csv_files", exist_ok=True)

# -------------------------------------------------------------------------------*/

def run_step(script):
    """
    Execute a sub-script using `uv run` and print progress.
    Args:
        script (str): Python script to run
    """
    print(f"▶️ {script}…")
    subprocess.run(["uv", "run", script], check=True)

# -------------------------------------------------------------------------------*/

def main():
    """
    Main workflow:
    1. Load environment variables
    2. Export guild structure
    3. Export all chat histories to a single CSV file
    """
    # Load environment variables from .env file (e.g., API tokens)
    load_dotenv()
    
    # Retrieve and save guild/channel structure
    run_step("discord_guild_channel_exporter.py")
    
    # Export all chat histories to a single CSV file
    run_step("discord_chat_history_exporter.py")
    
    print("✅ ETL pipeline completed successfully")

if __name__ == "__main__":
    main()