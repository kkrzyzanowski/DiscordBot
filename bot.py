import discord
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
print(f"Loaded TOKEN: {TOKEN}")
from getwykopposts import get_top_wykop_entries

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # test
    if message.content.startswith("!hello"):
        await message.channel.send("Hello!")

    # !wykop5
    if message.content.startswith("!wykop5"):
        try:
            entries = get_top_wykop_entries(5)
        except Exception as e:
            await message.channel.send(f"Błąd pobierania wpisów Wykop: {e}")
            return

        for i, e in enumerate(entries, 1):
            msg = f"""
🔥 #{i} Wykop ({e['votes']['up']} 👍)

👤 {e['author']['username']}

📝 {e['content']}

🔗 https://wykop.pl/wpis/{e['id']}
"""
            await message.channel.send(msg)

    # !wykop X
    elif message.content.startswith("!wykop"):
        try:
            parts = message.content.split()
            count = int(parts[1]) if len(parts) > 1 else 3
            count = min(count, 10)

            entries = get_top_wykop_entries(count)

            for i, e in enumerate(entries, 1):
                msg = f"""
🔥 #{i} Wykop ({e['votes']['up']} 👍)

👤 {e['author']['username']}

📝 {e['content']}

🔗 https://wykop.pl/wpis/{e['id']}
"""
                await message.channel.send(msg)

        except:
            await message.channel.send("Użycie: !wykop 5")


client.run(TOKEN)