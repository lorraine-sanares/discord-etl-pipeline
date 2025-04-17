import os
from dotenv import load_dotenv
import discord

# 读取 .env
load_dotenv()

# 从环境变量获取
TOKEN = os.getenv("DARCY_KEY")
TARGET_CHANNEL_ID = 1354790138802212984

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ Bot 已上线：{client.user}")

@client.event
async def on_message(message):
    # 只监听指定频道
    if message.channel.id != TARGET_CHANNEL_ID:
        return
    if message.author == client.user:
        return

    print(f"[{message.channel.name}] {message.author}: {message.content}")
    with open("g_chat_log.txt", "a", encoding="utf-8") as f:
        f.write(f"{message.author}: {message.content}\n")

client.run(TOKEN)

