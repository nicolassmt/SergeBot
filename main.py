import discord
from discord.ext import commands
import os

print("🚀 Démarrage du bot Serge...")

config = {
    "TOKEN": os.getenv("DISCORD_TOKEN"),
    "AUTHORIZED_ROLE_IDS": [1370723124865400902, 1370671598901788713],
    "SERGE_AVATAR_URL": "https://www.hebergeur-image.fr/uploads/20251011/9858ca780a9a005b8781f863e3dcb2150da21755.png",
    "SERGE_NAME": "Serge",
    "prefix": "!"
}

if not config["TOKEN"]:
    print("❌ ERREUR : Aucun token trouvé dans les variables d'environnement (DISCORD_TOKEN).")
    print("⚠️ Vérifie dans Render > Environment que la variable DISCORD_TOKEN est bien définie.")
    exit()

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

    webhook = await ctx.channel.create_webhook(name=config["SERGE_NAME"])
    await webhook.send(
        content=message,
        username=config["SERGE_NAME"],
        avatar_url=config["SERGE_AVATAR_URL"]
    )
    await webhook.delete()

print("⚙️ Lancement du bot...")
bot.run(config["TOKEN"])
