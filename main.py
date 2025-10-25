import discord
from discord.ext import commands
import os
import threading
from flask import Flask  # ✅ Nécessaire pour le keep-alive

print("🚀 Démarrage du bot Serge...")

# === CONFIGURATION ===
config = {
    "TOKEN": os.getenv("DISCORD_TOKEN"),
    "AUTHORIZED_ROLE_IDS": [1370723124865400902, 1370671598901788713],
    "SERGE_AVATAR_URL": "https://raw.githubusercontent.com/nicolassmt/SergeBot/main/assets/serge.png",
    "SERGE_NAME": "Serge",
    "prefix": "!"
}

if not config["TOKEN"]:
    print("❌ ERREUR : Aucun token trouvé dans les variables d'environnement (DISCORD_TOKEN).")
    print("⚠️ Vérifie dans Render > Environment que la variable DISCORD_TOKEN est bien définie.")
    exit()

# === KEEP-ALIVE (pour UptimeRobot) ===
app = Flask(__name__)

@app.route('/')
def home():
    print("📡 Ping reçu — UptimeRobot a vérifié la présence de Serge.")
    return "🌊 Serge veille toujours sur le lac..."

def run():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    thread = threading.Thread(target=run)
    thread.start()

# === DISCORD BOT ===
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=config["prefix"], intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Serge est en ligne sous le nom {bot.user} !")
    await bot.change_presence(activity=discord.Game("au bord du lac... 🌊"))

@bot.command()
@commands.has_any_role(*config["AUTHORIZED_ROLE_IDS"])
async def serge(ctx, *, message: str):
    """Remplace ton message par celui de Serge"""
    try:
        await ctx.message.delete()
    except discord.Forbidden:
        pass

    webhook = await ctx.channel.create_webhook(name=config["SERGE_NAME"])
    await webhook.send(
        content=message,
        username=config["SERGE_NAME"],
        avatar_url=config["SERGE_AVATAR_URL"]
    )
    await webhook.delete()

# === LANCEMENT ===
keep_alive()
print("⚙️ Lancement du bot...")
bot.run(config["TOKEN"])
