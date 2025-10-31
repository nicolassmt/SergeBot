import os
import asyncio
from flask import Flask
import threading
import discord
from discord.ext import commands

# === Flask app pour UptimeRobot ===
app = Flask(__name__)

@app.route('/')
def home():
    return "Serge est en ligne."

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

def keep_alive():
    t = threading.Thread(target=run)
    t.start()

# === Discord bot ===
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print("🚀 Démarrage du bot Serge...")
    print("⚙️ Lancement du bot...")
    print(f"✅ Connecté en tant que {bot.user}")

# === Commande principale : effet d’écriture progressive ===
@bot.command()
async def serge(ctx, *, message: str):
    # On tente de supprimer le message de commande pour garder la propreté
    try:
        await ctx.message.delete()
    except Exception:
        pass

    # On envoie un message vide pour commencer la "rédaction progressive"
    msg = await ctx.send("…")

    # Découpe le texte en blocs
    words = message.split(" ")
    display = ""
    step = 5   # Nombre de mots par bloc
    delay = 0.5  # Délai entre chaque bloc

    for i in range(0, len(words), step):
        display += " ".join(words[i:i + step]) + " "
        await msg.edit(content=display.strip())
        await asyncio.sleep(delay)

    # Petit effet final
    await asyncio.sleep(1)
    await msg.edit(content=display.strip() + " ░")

# === Lancement ===
keep_alive()
bot.run(os.getenv("DISCORD_TOKEN"))
