import asyncio
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import api

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
bot = commands.Bot(command_prefix="!")

@bot.command(name="stonks", description="show leaderboard")
async def stonks(ctx, *args):
    await api.main(ctx, args)

@bot.event
async def on_command_error(ctx, error):
    await ctx.send("ALLAH KAPUTTPUTT!!!:\n"+str(error))

@bot.event
async def on_ready():
    print("READY")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="seinem Geld beim wachsen zu"))

bot.run(TOKEN)