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
git clone https://github.com/supercarryleoliao/Dicord-bot-RAG.git
cd Dicord-bot-RAG
```

### 2. Install dependencies

```bash
pip install python-dotenv discord.py
```

Or, if you prefer:

```bash
pip install -r requirements.txt
```

### 3. Configure your credentials

Create a file named `.env` in the project root:

```dotenv
# .env
DARCY_KEY=<YOUR_DISCORD_BOT_TOKEN>
GUILD_ID=<YOUR_DISCORD_SERVER_ID>
```

> **Note:** Never commit your real `.env`—it’s already in `.gitignore`.

---

## 📝 Usage

### Export your server’s channel & thread structure

```bash
# With Python
python discord_guild_channel_exporter.py

# Or with 'uv' (if you have Uvicorn or another runner)
uv run discord_guild_channel_exporter.py
```

This will create `guild_channels_with_threads.json`:

```jsonc
{
  "guild_id": 123456789012345678,
  "guild_name": "My Server",
  "categories": [ /* … */ ],
  "ungrouped":    [ /* … */ ]
}
```

---

### Export a channel’s full message history

```bash
python discord_chat_history_exporter.py
```

1. The script reads `guild_channels_with_threads.json` and lists all text channels.  
2. Enter the **ID** of the channel whose history you want.  
3. It writes `<channel_id>_history.json`, e.g. `987654321098765432_history.json`:

```jsonc
[
  {
    "id": 111111111111111111,
    "author": "SomeUser",
    "content": "Hello, world!",
    "created_at": "2025-04-20T12:34:56.789000"
  },
  /* … */
]
```

---

## ⚙️ Configuration & Intents

- Make sure your bot in the [Discord Developer Portal](https://discord.com/developers/applications) has **Message Content Intent** enabled under **Bot → Privileged Gateway Intents**.  
- Your `.env` must contain the **bot token** (not the Application ID or Public Key).

---

## 📄 License

This project is released under the MIT License. See [LICENSE](LICENSE) for details.

---

## 🙋 Questions?

Feel free to open an issue or contact me at [ziang.liao@dscubed.org.au].  
Happy exporting! 🚀
