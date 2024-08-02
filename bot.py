import os
import discord
from discord.ext import commands
from pymongo import MongoClient
from datetime import datetime
import pytz

MONGO_URL = os.getenv('MONGO_URI')
if not MONGO_URL:
    raise RuntimeError("MongoDB URI (MONGO_URI) environment variable is not set")
client = MongoClient(MONGO_URL)
db = client.api_management
users_collection = db.users

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await bot.tree.sync()

@bot.tree.command(name="register_key")
async def register_key(interaction: discord.Interaction, key: str, key_type: str):
    if key_type not in ["basic", "pro"]:
        await interaction.response.send_message("Invalid key type. Use 'basic' or 'pro'.", ephemeral=True)
        return
    
    if users_collection.find_one({"api_key": key}):
        await interaction.response.send_message("API key already exists.", ephemeral=True)
        return

    users_collection.insert_one({
        "api_key": key,
        "key_type": key_type,
        "daily_count": 0,
        "last_reset": datetime.now(pytz.timezone('US/Eastern')) - timedelta(days=1)
    })
    await interaction.response.send_message("API key registered successfully.")

@bot.tree.command(name="delete_key")
async def delete_key(interaction: discord.Interaction, key: str):
    result = users_collection.delete_one({"api_key": key})
    if result.deleted_count:
        await interaction.response.send_message("API key deleted successfully.")
    else:
        await interaction.response.send_message("API key not found.")

@bot.tree.command(name="show_key")
async def show_key(interaction: discord.Interaction, key: str):
    user = users_collection.find_one({"api_key": key})
    if user:
        await interaction.response.send_message(f"API Key: {key}\nType: {user['key_type']}\nDaily Count: {user['daily_count']}")
    else:
        await interaction.response.send_message("API key not found.")

@bot.tree.command(name="show_usage")
async def show_usage(interaction: discord.Interaction):
    est = pytz.timezone('US/Eastern')
    now = datetime.now(est)
    users = users_collection.find()
    usage_summary = []

    for user in users:
        last_reset = user.get('last_reset', now - timedelta(days=1))
        if now >= last_reset + timedelta(days=1):
            daily_count = 0
        else:
            daily_count = user.get('daily_count', 0)

        usage_summary.append(f"API Key: {user['api_key']} - Daily Count: {daily_count}")

    if usage_summary:
        await interaction.response.send_message("\n".join(usage_summary))
    else:
        await interaction.response.send_message("No usage data available.")

bot.run('YOUR_BOT_TOKEN')
