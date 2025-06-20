import discord
import requests
import asyncio
import os

# === AMBIL DISCORD TOKEN DARI ENV ===
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
if not DISCORD_TOKEN:
    raise ValueError("❌ DISCORD_TOKEN belum diset di environment variable Railway!")

# === KONFIGURASI LANGSUNG DI SINI ===
CHANNEL_ID = 1384148467676483686  # ID channel target di Discord
TELEGRAM_BOT_TOKEN = '7848618432:AAFJESYJF-0hXIwvLABuDTDcL8zNk2cB5SM'
TELEGRAM_CHAT_ID = '5802965692'

# === KATA-KATA KUNCI YANG AKAN DIDETEKSI ===
KEYWORDS = ['carrot', 'tomato', 'blueberry']

# === FUNGSI SPAM KE TELEGRAM ===
async def spam_telegram(pesan, jumlah=8, interval=0.5):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    data = {'chat_id': TELEGRAM_CHAT_ID, 'text': pesan}
    for i in range(jumlah):
        try:
            response = requests.post(url, data=data)
            if response.status_code != 200:
                print(f'❌ Gagal kirim pesan ke Telegram (ke-{i+1}): {response.text}')
            else:
                print(f'✅ Terkirim ke Telegram (ke-{i+1})')
        except Exception as e:
            print(f'❌ Error saat kirim ke Telegram (ke-{i+1}): {e}')
        await asyncio.sleep(interval)

# === BOT DISCORD ===
class MyClient(discord.Client):
    async def on_ready(self):
        print(f'✅ Bot berhasil login sebagai {self.user}')

    async def on_message(self, message):
        if message.channel.id != CHANNEL_ID:
            return
        if message.author.bot:
            return

        for keyword in KEYWORDS:
            if keyword.lower() in message.content.lower():
                print(f'🚨 Deteksi keyword: "{keyword}" di pesan: {message.content}')
                pesan = f'📢 Deteksi kata: "{keyword}" di Discord!\n\n📨 Pesan:\n{message.content}'
                await spam_telegram(pesan)
                break

# === JALANKAN BOT ===
intents = discord.Intents.default()
intents.message_content = True  # Penting untuk baca isi pesan!

client = MyClient(intents=intents)
client.run(DISCORD_TOKEN)
