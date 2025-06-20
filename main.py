import discord
import requests
import asyncio
import os

# === AMBIL DISCORD TOKEN DARI ENV ===
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# === KONFIGURASI (TIDAK DARI ENV) ===
CHANNEL_ID = 1384148467676483686  # ID channel #gagstock
TELEGRAM_BOT_TOKEN = '7848618432:AAFJESYJF-0hXIwvLABuDTDcL8zNk2cB5SM'
TELEGRAM_CHAT_ID = '5802965692'

# === KATA-KATA YANG AKAN DIDETEKSI ===
KEYWORDS = ['carrot', 'tomato', 'blueberry']

# === CEK APAKAH DISCORD TOKEN ADA ===
if not DISCORD_TOKEN:
    raise ValueError("❌ DISCORD_TOKEN belum diset di environment variable!")

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
