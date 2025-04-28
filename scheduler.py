"""
Weekly Ingestion Scheduler

This script runs the Discord ETL Pipeline every week at a specified day/time.

Requirements:
  pip install schedule python-dotenv

Usage:
  $ python scheduler.py
"""

import os
import subprocess
import schedule
import time
from dotenv import load_dotenv

# Load .env to ensure environment variables are available for subscripts
def load_env():
    load_dotenv()

# Function to invoke the existing ETL pipeline
def ingest_data():
    load_env()
    print("🔄 Starting weekly ingestion...")
    try:
        subprocess.run(["uv", "run", "discord_etl_pipeline.py"], check=True)
        print("✅ Weekly ingestion completed.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Ingestion failed: {e}")

# Schedule: every Monday at 02:00 AM
schedule.every().monday.at("02:00").do(ingest_data)

if __name__ == "__main__":
    print("🗓️ Scheduler started: will run weekly ingestion on Mondays at 02:00 AM")
    # Run once at startup
    ingest_data()
    # Loop to keep scheduler alive
    while True:
        schedule.run_pending()
        time.sleep(60)