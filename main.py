import os
import asyncio
import discord
from discord.ext import commands
from flask import Flask
import threading

print("🚀 Démarrage du bot Serge...")

# === CONFIGURATION ===
config = {
    "TOKEN": os.getenv("DISCORD_TOKEN"),
    "SERGE_AVATAR_URL": "https://github.com/nicolassmt/SergeBot/raw/main/assets/serge.png",
    "SERGE_NAME": "Serge",
    "prefix": "!"
}

if not config["TOKEN"]:
    print("❌ ERREUR : Aucun token trouvé dans les variables d'environnement (DISCORD_TOKEN).")
    exit()

# === KEEP ALIVE ===
app = Flask(__name__)

@app.route('/')
def home():
    return "🌊 Serge veille toujours sur le lac..."

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

def keep_alive():
    t = threading.Thread(target=run)
    t.start()

# === DISCORD BOT ===
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=config["prefix"], intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Serge est en ligne sous le nom {bot.user} !")
    await bot.change_presence(activity=discord.Game("au bord du lac... 🌊"))

# === COMMANDE SERGE ===
@bot.command()
async def serge(ctx, *, message: str):
    """Message dynamique façon 'speech to text'"""
    try:
        await ctx.message.delete()
    except discord.Forbidden:
        pass

    text = message.replace("\\n", "\n")

    # Crée le webhook pour parler avec l’avatar de Serge
    webhook = await ctx.channel.create_webhook(name=config["SERGE_NAME"])
    msg = await webhook.send(
        content="…", 
        username=config["SERGE_NAME"], 
        avatar_url=config["SERGE_AVATAR_URL"], 
        wait=True
    )

    display = ""
    delay = 0.25
    step = 5
    words = text.split(" ")

    # Construction progressive du message
    for i in range(0, len(words), step):
        display += " ".join(words[i:i + step]) + " "
        await webhook.edit_message(msg.id, content=display.strip())
        await asyncio.sleep(delay)

    # Finalise le message
    await webhook.edit_message(msg.id, content=display.strip())
    await webhook.delete()

# === LANCEMENT ===
keep_alive()
print("⚙️ Lancement du bot...")
bot.run(config["TOKEN"])

