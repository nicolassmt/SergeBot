import os
import discord
from discord.ext import commands
import json

# Charger la configuration depuis config.json
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=config["prefix"], intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Serge est en ligne sous le nom {bot.user} !")

@bot.command()
@commands.has_any_role(*config["AUTHORIZED_ROLE_IDS"])
async def serge(ctx, *, message: str):
    """Remplace ton message par celui de Serge"""
    try:
        await ctx.message.delete()
    except discord.Forbidden:
        pass

    # Crée un webhook pour que le message paraisse venir de Serge
    webhook = await ctx.channel.create_webhook(name=config["SERGE_NAME"])
    await webhook.send(
        content=message,
        username=config["SERGE_NAME"],
        avatar_url=config["SERGE_AVATAR_URL"]
    )
    await webhook.delete()

# --- GESTION DU TOKEN SÉCURISÉ ---
# On essaye d'abord de le récup
