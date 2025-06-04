import os
import discord
from discord.ext import commands
import requests
from dotenv import load_dotenv

# Tải biến môi trường
load_dotenv()
XAI_API_KEY = os.getenv("XAI_API_KEY")
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Cấu hình bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# URL endpoint của API Grok
API_URL = "https://api.x.ai/v1/chat/completions"

# Hàm gọi API Grok
def get_grok_response(message):
    headers = {
        "Authorization": f"Bearer {XAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "grok-beta",  # Mô hình Grok beta, có thể thay bằng "grok-3" nếu hỗ trợ
        "messages": [{"role": "user", "content": message}],
        "max_tokens": 150  # Giới hạn độ dài phản hồi
    }
    response = requests.post(API_URL, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Lỗi API: {response.status_code} - {response.text}"

# Sự kiện khi bot sẵn sàng
@bot.event
async def on_ready():
    print(f"Bot đã đăng nhập: {bot.user}")

# Lệnh !start
@bot.command()
async def start(ctx):
    await ctx.send("Chào! Tôi là bot Grok. Dùng !ask <câu hỏi> để trò chuyện!")

# Lệnh !ask
@bot.command()
async def ask(ctx, *, question):
    try:
        response = get_grok_response(question)
        await ctx.send(response)
    except Exception as e:
        await ctx.send(f"Lỗi: {str(e)}")

# Xử lý tin nhắn
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if not message.content.startswith("!"):
        try:
            response = get_grok_response(message.content)
            await message.channel.send(response)
        except Exception as e:
            await message.channel.send(f"Lỗi: {str(e)}")
    await bot.process_commands(message)

# Chạy bot
bot.run(DISCORD_BOT_TOKEN)
