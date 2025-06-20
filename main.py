import discord import requests import asyncio import os

=== AMBIL DISCORD TOKEN DARI ENV ===

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN') if not DISCORD_TOKEN: raise ValueError("\u274c DISCORD_TOKEN belum diset di environment variable!")

=== KONFIGURASI (LANGSUNG DITULIS DALAM SCRIPT) ===

CHANNEL_ID = 1384148467676483686  # Channel tempat deteksi keyword TELEGRAM_BOT_TOKEN = '7848618432:AAFJESYJF-0hXIwvLABuDTDcL8zNk2cB5SM' TELEGRAM_CHAT_ID = '5802965692' KEYWORDS = ['carrot', 'tomato', 'blueberry']

=== FUNGSI UNTUK KIRIM PESAN TELEGRAM ===

async def spam_telegram(pesan, jumlah=8, interval=0.5): url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage' data = {'chat_id': TELEGRAM_CHAT_ID, 'text': pesan} for i in range(jumlah): try: response = requests.post(url, data=data) print(f"\u2709\ufe0f Telegram Response ({i+1}):", response.status_code, response.text) except Exception as e: print(f'\u274c Gagal kirim ke Telegram: {e}') await asyncio.sleep(interval)

=== CLIENT DISCORD ===

class MyClient(discord.Client): async def on_ready(self): print(f'\u2705 Bot berhasil login sebagai {self.user}')

async def on_message(self, message):
    if message.channel.id != CHANNEL_ID or message.author.bot:
        return

    for keyword in KEYWORDS:
        if keyword.lower() in message.content.lower():
            print(f'\ud83d\udea8 Deteksi keyword: "{keyword}" di pesan: {message.content}')
            pesan = f'\ud83d\udce2 Deteksi kata: "{keyword}" di Discord!\nIsi pesan:\n{message.content}'
            await spam_telegram(pesan)
            break

=== INTENTS DAN JALANKAN BOT ===

intents = discord.Intents.default() intents.message_content = True

client = MyClient(intents=intents) client.run(DISCORD_TOKEN)

