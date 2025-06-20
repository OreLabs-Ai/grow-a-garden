import discord
import requests
import asyncio
import os

# === Ambil ENV dan Validasi ===
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Validasi semua ENV wajib ada
if not all([DISCORD_TOKEN, CHANNEL_ID, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID]):
    raise ValueError("❌ Pastikan semua ENV variable sudah diset di Railway!")

try:
    CHANNEL_ID = int(CHANNEL_ID)
except ValueError:
    raise ValueError("❌ CHANNEL_ID harus berupa angka!")

# === Kata yang dideteksi ===
KEYWORDS = ['carrot', 'tomato', 'blueberry']

# === Fungsi spam telegram ===
async def spam_telegram(pesan, jumlah=8, interval=0.5):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    data = {'chat_id': TELEGRAM_CHAT_ID, 'text': pesan}
    for i in range(jumlah):
        try:
            response = requests.post(url, data=data)
            print(f'📨 [{i+1}] Status Telegram: {response.status_code}')
        except Exception as e:
            print(f'❌ Error kirim telegram: {e}')
        await asyncio.sleep(interval)

# === Discord Bot Client ===
class MyClient(discord.Client):
    async def on_ready(self):
        print(f'✅ Bot login sebagai {self.user}')

    async def on_message(self, message):
        if message.channel.id != CHANNEL_ID:
            return
        if message.author.bot:
            return

        for keyword in KEYWORDS:
            if keyword.lower() in message.content.lower():
                print(f'🚨 Keyword "{keyword}" terdeteksi!')
                pesan = f'📢 Terdeteksi kata "{keyword}"!\nPesan:\n{message.content}'
                await spam_telegram(pesan)
                break

# === Jalankan Bot ===
intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(DISCORD_TOKEN)
