import discord
import requests
import asyncio

# === KONFIGURASI ===
DISCORD_TOKEN = 'MTMzNDc2ODY5NjYyMjcxNDk4NA.G1uLGp.PAfcPMYiwPL3wsP6_vm7Zxg_yi9WpoOY3el6iM'
CHANNEL_ID = 1384148467676483686  # ID channel #gagstock

KEYWORDS = ['carrot', 'tomato', 'blueberry']

TELEGRAM_BOT_TOKEN = '7848618432:AAFJESYJF-0hXIwvLABuDTDcL8zNk2cB5SM'
TELEGRAM_CHAT_ID = '5802965692'

# === FUNGSI KIRIM TELEGRAM (SPAM 8x per 4 detik) ===
async def spam_telegram(pesan, jumlah=8, interval=0.5):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    data = {'chat_id': TELEGRAM_CHAT_ID, 'text': pesan}
    for _ in range(jumlah):
        requests.post(url, data=data)
        await asyncio.sleep(interval)

# === CLIENT DISCORD ===
class MyClient(discord.Client):
    async def on_ready(self):
        print(f'✅ Bot login sebagai {self.user}')

    async def on_message(self, message):
        if message.channel.id != CHANNEL_ID or message.author.bot:
            return

        for keyword in KEYWORDS:
            if keyword.lower() in message.content.lower():
                print(f'🚨 Deteksi: "{keyword}" dalam pesan: {message.content}')
                pesan = f'📢 Deteksi kata: "{keyword}" di Discord!\nIsi pesan:\n{message.content}'
                await spam_telegram(pesan)
                break

# === JALANKAN BOT ===
intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(DISCORD_TOKEN)
