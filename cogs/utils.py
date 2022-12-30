import discord 
from discord.ext import commands
from discord import app_commands

class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("utils.py is ready!")
    
    @commands.command()
    async def ping(self, ctx):
        bot_latency = round(self.bot.latency * 1000)
        await ctx.send(f"Pong! {bot_latency} ms.")

    @commands.command()
    async def hi(self, ctx):
        await ctx.send(f"Hey! {ctx.author.mention}! This is a slash command!")

    @commands.command()
    @app_commands.describe(arg = "What should I say?")
    async def say(interaction: discord.Interaction, arg: str):
        await interaction.response.send_message(f"{interaction.user.name} said: '{arg}'")


async def setup(bot):
    await bot.add_cog(Utils(bot))
