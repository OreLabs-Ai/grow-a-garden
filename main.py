import discord
import requests
import asyncio
import os

# === AMBIL DATA DARI ENVIRONMENT VARIABLE ===
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# === KATA-KATA YANG AKAN DIDETEKSI ===
KEYWORDS = ['carrot', 'tomato', 'blueberry']

# === FUNGSI UNTUK SPAM TELEGRAM ===
async def spam_telegram(pesan, jumlah=8, interval=0.5):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    data = {'chat_id': TELEGRAM_CHAT_ID, 'text': pesan}
    for _ in range(jumlah):
        try:
            requests.post(url, data=data)
        except Exception as e:
            print(f'❌ Gagal kirim ke Telegram: {e}')
        await asyncio.sleep(interval)

# === KELAS BOT DISCORD ===
class MyClient(discord.Client):
    async def on_ready(self):
        print(f'✅ Bot berhasil login sebagai {self.user}')

    async def on_message(self, message):
        if message.channel.id != CHANNEL_ID or message.author.bot:
            return

        for keyword in KEYWORDS:
            if keyword.lower() in message.content.lower():
                print(f'🚨 Deteksi keyword: "{keyword}" di pesan: {message.content}')
                pesan = f'📢 Deteksi kata: "{keyword}" di Discord!\nIsi pesan:\n{message.content}'
                await spam_telegram(pesan)
                break

# === JALANKAN BOTNYA ===
intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(DISCORD_TOKEN)
