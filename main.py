# teétah
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import openai

# Tải biến môi trường
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Cấu hình bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Sự kiện khi bot sẵn sàng
@bot.event
async def on_ready():
    print(f"Bot đã đăng nhập: {bot.user}")
    channel = bot.get_channel(1283730671059206157)  # Thay YOUR_CHANNEL_ID
    if channel:
        await channel.send(f"Bot {bot.user} đã khởi động!")

# Lệnh !start
@bot.command()
async def start(ctx):
    await ctx.send("Chào! Tôi là bot ChatGPT. Gửi tin nhắn hoặc dùng !ask <câu hỏi>!")

# Lệnh !ask
@bot.command()
async def ask(ctx, *, question):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": question}]
        )
        await ctx.send(response.choices[0].message.content)
    except Exception as e:
        await ctx.send(f"Lỗi: {str(e)}")

# Xử lý tin nhắn
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if not message.content.startswith("!"):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": message.content}]
            )
            await message.channel.send(response.choices[0].message.content)
        except Exception as e:
            await message.channel.send(f"Lỗi: {str(e)}")
    await bot.process_commands(message)

# Chạy bot
bot.run(DISCORD_BOT_TOKEN)
