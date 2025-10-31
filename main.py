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
    # Supprime la commande initiale pour propreté
    try:
        await ctx.message.delete()
    except Exception:
        pass

    # Transforme le message pour conserver les retours à la ligne
    text = message.replace("\\n", "\n")

    # Envoie un message vide pour le construire dynamiquement
    msg = await ctx.send("…")

    display = ""
    delay = 0.25  # délai entre chaque "bloc" de mots
    step = 5      # nombre de mots ajoutés à chaque étape

    # Découpe le texte en blocs
    words = text.split(" ")

    for i in range(0, len(words), step):
        display += " ".join(words[i:i + step]) + " "
        await msg.edit(content=display.strip())
        await asyncio.sleep(delay)

    # Laisse la dernière version en place (pas de doublon)
    await asyncio.sleep(0.5)
    await msg.edit(content=display.strip())

# === Lancement ===
keep_alive()
bot.run(os.getenv("DISCORD_TOKEN"))
