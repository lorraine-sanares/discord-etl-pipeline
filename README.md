# Discord Channel & History Exporter

A set of Python scripts that use the [discord.py](https://github.com/Rapptz/discord.py) library to:

1. **Export your server’s channel structure** (categories, text/forums, threads) into JSON.  
2. **Interactively fetch a single channel’s full message history** into JSON.

---

## 📦 Contents

- **`.env`** – your bot credentials (ignored by Git)  
- **`.gitignore`** – ignores `.env`, logs, JSON exports, etc.  
- **`discord_guild_channel_exporter.py`** – exports every category, channel & active thread  
- **`discord_chat_history_exporter.py`** – prompts for a channel ID and exports its message history  
- **`bot_demo.py`** – a minimal “hello world” Discord bot example  
- **`main.py`** – (optional) your own orchestration or demo entrypoint  
- **`*.json` / `*.txt`** – sample/exported data (e.g. `guild_channels_with_threads.json`, `123456789_history.json`)  
- **`pyproject.toml`**, **`uv.lock`** – project metadata & lockfiles  
- **`LICENSE`** – MIT License  

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/your‑username/discord‑exporter.git
cd discord‑exporter
