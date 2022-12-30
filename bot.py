import discord 
from discord import app_commands
from discord.ext import commands
import json
import sys
import os
import asyncio

bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())

bot.toggle = False

@bot.event
async def on_ready():
    print("Bot is up and ready!")
    try:
            synced = await bot.tree.sync()
            print(f"Synced {len(synced)} command(s)")
    except Exception as e:
            print(e)

async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"{filename[:-3]} is loaded!")

@bot.tree.command(name = "reload") 
async def reload(interaction: discord.Interaction):
    for filename in os.listdir('./cogs'):
        bot.reload_extension(f"cogs.{filename[:-3]}")
        await interaction.response.send_message(f"Reloaded {filename[:-3]}!")

@bot.tree.command(name = "hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hey! {interaction.user.mention}! This is a slash command!", ephemeral=True)

@bot.tree.command(name = "say")
@app_commands.describe(arg = "What should I say?")
async def say(interaction: discord.Interaction, arg: str):
    await interaction.response.send_message(f"{interaction.user.name} said: '{arg}'")

@bot.tree.command(name = "toggle")
async def toggle(interaction: discord.Interaction):
    bot.toggle = not bot.toggle
    ternary = "on" if bot.toggle else "off"
    await interaction.response.send_message(f"GPT mode has been toggled to {ternary}!")

def restart_bot(): 
  os.execv(sys.executable, ['python'] + sys.argv)

@bot.tree.command(name = "restart")
async def restart(interaction:discord.Interaction):
  await interaction.response.send_message("Restarting bot...")
  restart_bot()

@bot.tree.command(name = "close")
@commands.has_permissions(administrator=True)
async def close(interaction: discord.Interaction):
    await interaction.response.send_message(f"Shutting down!")
    await bot.close()

async def run_bot():
    async with bot:
        await load()
        with open('config.json') as config_file:
            data = json.load(config_file)
            token = data['TOKEN']
        await bot.start(token)
    
asyncio.run(run_bot())
     







    