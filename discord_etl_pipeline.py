"""
    Discord ETL Pipeline
    
    This scripts automates ingestion of discord data, transforms it into a csv file
    
    The program utilises functions:
        - discord_guild_channel_exporter.py to extract the channels in the server
        - discord_chat_history_exporter.py to extract entire chat history
        
    Key Features:
        - Automated data ingestion to get most frequent messages
        - Filter functions to extract specific info Darcy needs?
        - Loads data into an AWS RDS database
        
    Environment Variables Required:

"""

import os
import json
from dotenv import load_dotenv
import pandas as pd
import discord_guild_channel_exporter
import discord_chat_history_exporter

# load_dotenv()
# TOKEN = os.getenv("DARYL_KEY")               # Discord bot token
# GUILD_ID = int(os.getenv("TEST_SERVER_ID"))        # Target server ID (converted to int)



# -----------------------------------------------------------------------------
# 1. Load JSON data from files
# -----------------------------------------------------------------------------

with open("1219232033545519116_history.json", "r") as f:
    messages = json.load(f)
    
# -----------------------------------------------------------------------------
# 2. Parsing into dataframe
# -----------------------------------------------------------------------------

def export_chat_history(json_path: str, csv_path: str):
    # 1. Load raw JSON messages
    with open(json_path, "r") as f:
        messages = json.load(f)

    # 2. Create DataFrame
    df = pd.DataFrame(messages)

    # 3. Parse the timestamp strings into pandas datetime
    df['created_at'] = pd.to_datetime(
        df['created_at'],
        format='ISO8601',
        utc=True
    )


    # 4. (Optional) Use the timestamp as the index for time-based operations
    df.set_index('created_at', inplace=True)

    # 5. Save to CSV
    df.to_csv(csv_path, index=True)
    print(f"Exported {len(df)} messages to {csv_path}")

if __name__ == "__main__":
    export_chat_history("1219232033545519116_history.json", "chat_history.csv")