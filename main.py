import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

valorant_role = "Valorant"
tft_role = "Teamfight Tactics"
lol_role = "League of Legends"

@bot.event
async def on_ready():
    print(f"We are ready to log in, {bot.user.name}")

@bot.event
async def on_member_join(member):
    await member.send(f"Welcome to the server {member.name}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "zee" in message.content.lower():
        await message.delete()
        await message.channel.send(f"{message.author.mention} - wag mo banggitin yan!")

    await bot.process_commands(message)

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}!")

@bot.command()
async def lil(ctx):
    await ctx.send(f"Sleeping {ctx.author.mention}!")

@bot.command()
async def tiktok(ctx):
    await ctx.send(f"https://www.tiktok.com/@shanghaispicy {ctx.author.mention}!")

@bot.command()
async def rank(ctx):
    await ctx.send(f"Radiant {ctx.author.mention}!")

@bot.command()
async def aiz(ctx):
    await ctx.send(f"soft spoken clove main yan hehe sarap {ctx.author.mention}!")

@bot.command()
async def valorant(ctx):
    role = discord.utils.get(ctx.guild.roles, name=valorant_role)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} is now assigned to {valorant_role}!")
    else:
        await ctx.send("Role doesn't exist")

@bot.command()
async def tft(ctx):
    role = discord.utils.get(ctx.guild.roles, name=tft_role)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} is now assigned to {tft_role}!")
    else:
        await ctx.send("Role doesn't exist")

@bot.command()
async def lol(ctx):
    role = discord.utils.get(ctx.guild.roles, name=lol_role)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} is now assigned to {lol_role}!")
    else:
        await ctx.send("Role doesn't exist")

@bot.command()
async def lilcommands(ctx):
    await ctx.reply("!hello, !lil, !tiktok, !rank, !aiz")

@bot.command()
async def poll(ctx, *, question):
    embed = discord.Embed(title="THOUGHTS NI LIL", description=question, color=discord.Color.green())
    poll_message = await ctx.send(embed=embed)
    await poll_message.add_reaction("👍")
    await poll_message.add_reaction("👎")

bot.run(token,  log_handler=handler, log_level=logging.DEBUG)