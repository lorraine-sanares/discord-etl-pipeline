import os
import discord
from dotenv import load_dotenv

# 加载 .env
load_dotenv()
TOKEN = os.getenv("DARCY_KEY")
CHANNEL_ID = 1354790138802212984

# 设置 intents，允许读取消息内容
intents = discord.Intents.default()
intents.message_content = True

# 创建客户端
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ Bot 已上线：{client.user}")
    channel = client.get_channel(CHANNEL_ID)
    if channel is None:
        print(f"❌ 找不到频道 ID：{CHANNEL_ID}")
        await client.close()
        return

    all_messages = []
    before = None

    print("开始分页拉取历史消息…")
    while True:
        # 每次最多取 100 条，更早的消息由 before 控制
        history = await channel.history(limit=100, before=before).flatten()
        if not history:
            break
        all_messages.extend(history)
        before = history[-1].created_at  # 更新 before 到最早一条的时间
        print(f"已拉取 {len(all_messages)} 条，还在继续…")

    # 反转列表，让最早的消息排在最前面
    all_messages.reverse()

    # 写入文件
    out_path = "g_chat_full_history.txt"
    with open(out_path, "w", encoding="utf-8") as f:
        for msg in all_messages:
            timestamp = msg.created_at.strftime("%Y-%m-%d %H:%M:%S")
            line = f"[{timestamp}] {msg.author}：{msg.content}"
            f.write(line + "\n")

    print(f"✅ 共拉取 {len(all_messages)} 条消息，已保存到 `{out_path}`")
    await client.close()

# 启动
client.run(TOKEN)
