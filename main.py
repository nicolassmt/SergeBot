import discord
from discord import app_commands
import json

# Chargement du fichier config.json
with open("config.json", "r") as f:
    config = json.load(f)

TOKEN = config["TOKEN"]
AUTHORIZED_ROLE_IDS = config["AUTHORIZED_ROLE_IDS"]
SERGE_AVATAR_URL = config["SERGE_AVATAR_URL"]
SERGE_NAME = config.get("SERGE_NAME", "Serge")

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

@bot.event
async def on_ready():
    await tree.sync()
    print(f"✅ Serge est prêt à parler sur {len(bot.guilds)} serveur(s)")

@tree.command(name="serge", description="Fait parler Serge dans ce salon (avec avatar).")
async def serge(interaction: discord.Interaction, message: str):
    user_roles = [role.id for role in interaction.user.roles]
    if not any(role_id in user_roles for role_id in AUTHORIZED_ROLE_IDS):
        await interaction.response.send_message(
            "⛔ T’as pas l’droit d’parler pour moi, étranger.",
            ephemeral=True
        )
        return

    # Vérifie ou crée un webhook dans le salon
    webhooks = await interaction.channel.webhooks()
    serge_webhook = discord.utils.get(webhooks, name=SERGE_NAME)

    if not serge_webhook:
        serge_webhook = await interaction.channel.create_webhook(name=SERGE_NAME, avatar=None)

    # Envoie le message en utilisant le webhook (apparence d'un joueur)
    await serge_webhook.send(
        content=f"**{SERGE_NAME} :** {message}",
        username=SERGE_NAME,
        avatar_url=SERGE_AVATAR_URL
    )

    await interaction.response.send_message("✅ Serge a parlé.", ephemeral=True)

bot.run(TOKEN)
