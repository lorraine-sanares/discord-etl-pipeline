# Discord ETL Pipeline

A simple Python ETL pipeline to extract Discord channel and message data, transform chat history JSON into CSV, and prepare it for loading into an AWS RDS database — all automated on a weekly schedule.

---

## 📦 Contents

- **`.env`** – your bot & AWS credentials (ignored by Git)
- **`.gitignore`** – ignores `.env`, logs, JSON exports, etc.
- **`json_files/`** – stores all exported JSON: guild structure + channel histories
- **`csv_files/`** – stores all generated CSV chat logs
- **`discord_guild_channel_exporter.py`** – exports guild channels into `json_files/guild_channels_with_threads.json`
- **`discord_chat_history_exporter.py`** – batch‑exports every text channel’s history into `json_files/<channel_name>_history.json`
- **`discord_etl_pipeline.py`** – orchestrates exporters and transforms all JSON to CSV in `csv_files/`
- **`scheduler.py`** – runs the full pipeline weekly via Python scheduler
- **`pyproject.toml`**, **`uv.lock`** – project metadata & lockfiles
- **`LICENSE`** – MIT License

---

## ⚙️ Requirements

- Python 3.12+
- Dependencies:
  ```bash
  pip install python-dotenv discord-py pandas requests schedule
  ```

---

## 🔧 Configuration

Create a `.env` file in the project root:

```env
# Discord
DARCY_KEY=<YOUR_DISCORD_BOT_TOKEN>
TEST_SERVER_ID=<YOUR_DISCORD_SERVER_ID>

# (Optional) AWS RDS — extend the pipeline to load CSV into RDS
AWS_HOST=<YOUR_RDS_HOST>
AWS_PORT=<YOUR_RDS_PORT>
AWS_DB=<YOUR_RDS_DATABASE>
AWS_USER=<YOUR_RDS_USERNAME>
AWS_PASSWORD=<YOUR_RDS_PASSWORD>
```

> **Never commit** your real `.env` — it’s already in `.gitignore`.

---
## Before Using

Run this command in the terminal:

```bash
export SSL_CERT_FILE=$(python -m certifi)
```

## 🚀 Usage

All scripts can be run via `uv run <script>.py`, but you can also call them with plain `python`.

### 1. Export guild structure

```bash
uv run discord_guild_channel_exporter.py
```
Creates:
```
json_files/guild_channels_with_threads.json
```

### 2. Export all channel histories

```bash
uv run discord_chat_history_exporter.py
```
Creates one JSON per text channel:
```
json_files/general_history.json
json_files/random_history.json
... etc.
```

### 3. Full ETL: JSON → CSV

```bash
uv run discord_etl_pipeline.py
```
This will:
1. Re‑export guild structure & histories
2. Convert each `*_history.json` to `csv_files/<channel_name>_chat_history.csv`

### 4. (Optional) Run once via scheduler

To automate weekly ingestion (Monday at 02:00 AM local):

```bash
python scheduler.py
```
Or integrate into a systemd/cron job if you prefer.

---

## 📄 License

Released under the MIT License. See [LICENSE](LICENSE) for details.

---

## ❓ Questions?

Open an issue or ping me at lorraine.sanares@dscubed.org.au — happy exporting! 🚀

