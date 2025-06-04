import os
import discord
from discord.ext import commands
import openai  # Sử dụng OpenAI SDK, tương thích với Grok

# Tải biến môi trường
load_dotenv()
openai.api_key = os.getenv("XAI_API_KEY")  # Thay bằng XAI_API_KEY
openai.api_base = "https://api.x.ai/v1"  # Endpoint của Grok API

# Cấu hình bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

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
        response = openai.ChatCompletion.create(
            model="grok-beta",  # Sử dụng mô hình Grok beta
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
                model="grok-beta",
                messages=[{"role": "user", "content": message.content}]
            )
            await message.channel.send(response.choices[0].message.content)
        except Exception as e:
            await message.channel.send(f"Lỗi: {str(e)}")
    await bot.process_commands(message)

# Chạy bot
bot.run(os.getenv("DISCORD_BOT_TOKEN"))
