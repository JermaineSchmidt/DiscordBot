import discord
from discord.ext import commands
import random
import youtube_dl
import json
import os

# Load config file
with open('config.json') as config_file:
    config = json.load(config_file)

# Setup intents and bot
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix=config['prefix'], intents=intents)

# Help Command
@bot.command()
async def help(ctx):
    help_text = """
    **Commands:**
    `!help` - Shows this message.
    `!kick @user` - Kicks a member from the server.
    `!ban @user` - Bans a member from the server.
    `!mute @user` - Mutes a member.
    `!8ball [question]` - Answers a yes/no question.
    `!weather [city]` - Shows the weather in the specified city.
    `!play [url]` - Plays music from YouTube.
    """
    await ctx.send(help_text)

# Kick Command
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'{member.mention} has been kicked.')

# Ban Command
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'{member.mention} has been banned.')

# Mute Command
@bot.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member):
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not muted_role:
        muted_role = await ctx.guild.create_role(name="Muted")
        for channel in ctx.guild.channels:
            await channel.set_permissions(muted_role, speak=False, send_messages=False)
    await member.add_roles(muted_role)
    await ctx.send(f'{member.mention} has been muted.')

# 8Ball Command
@bot.command()
async def 8ball(ctx, *, question):
    responses = [
        "Yes, definitely.",
        "No, certainly not.",
        "Maybe.",
        "I cannot tell right now.",
        "Ask again later."
    ]
    await ctx.send(f'🎱 {random.choice(responses)}')

# Weather Command
@bot.command()
async def weather(ctx, *, city):
    # Placeholder: Replace with actual API call to fetch weather data
    await ctx.send(f'The current weather in {city} is sunny.')

# Music Command
@bot.command()
async def play(ctx, url):
    voice_channel = discord.utils.get(ctx.guild.voice_channels, name='General')
    if not voice_channel:
        await ctx.send("Voice channel not found!")
        return
    
    vc = await voice_channel.connect()
    
    with youtube_dl.YoutubeDL({'format': 'bestaudio'}) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        vc.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=url2))
    
    await ctx.send(f'Playing: {info["title"]}')

# Event: On Ready
@bot.event
async def on_ready():
    print(f'Bot is ready as {bot.user}')

# Run the bot with the token from config.json
bot.run(config['token'])
