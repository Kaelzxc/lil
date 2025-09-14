import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import random
import aiohttp
import json
from flask import Flask
import threading


# ========== FLASK APP FOR RENDER HOSTING ==========
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

# Start Flask app in a separate thread
flask_thread = threading.Thread(target=run_flask)
flask_thread.start()

# ========== DISCORD BOT SETUP ==========
load_dotenv()

# ========== DISCORD BOT SETUP ==========
load_dotenv()
token = os.getenv('DISCORD_TOKEN')
GIPHY_API_KEY = os.getenv('GIPHY_API_KEY')  # Put your Giphy API key in .env

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

valorant_role = "Valorant"
tft_role = "Teamfight Tactics"
lol_role = "League of Legends"

# ===== STATUS FILES =====
LIL_STATUS_FILE = "CHI_status.json"
SAV_STATUS_FILE = "SAV_status.json"
YUKS_STATUS_FILE = "YUKS_status.json"

# ===== STATUS LOADERS =====
def load_status(file):
    try:
        with open(file, "r") as f:
            return json.load(f).get("status", None)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def save_status(file, status):
    with open(file, "w") as f:
        json.dump({"status": status}, f)

# Initial status values
lil_status = load_status(LIL_STATUS_FILE)
sav_status = load_status(SAV_STATUS_FILE)
yuks_status = load_status(YUKS_STATUS_FILE)

async def fetch_giphy_gif(search_term):
    async with aiohttp.ClientSession() as session:
        url = "https://api.giphy.com/v1/gifs/search"
        params = {
            "api_key": GIPHY_API_KEY,
            "q": search_term,
            "limit": 25,
            "offset": 0,
            "rating": "pg-13",
            "lang": "en"
        }
        async with session.get(url, params=params) as resp:
            if resp.status == 200:
                data = await resp.json()
                gifs = data.get("data")
                if gifs:
                    chosen = random.choice(gifs)
                    return chosen["images"]["original"]["url"]
    return None

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

    content = message.content.lower()

    # Auto-replies for greetings
    if "goodmorning" in content or "good morning" in content:
        await message.channel.send(f"Good morning, {message.author.mention}! ☀️")
    elif "goodnight" in content or "good night" in content:
        await message.channel.send(f"Good night, {message.author.mention}! 🌙")
    elif "hello" in content:
        await message.channel.send(f"Hello there, {message.author.mention}! 👋")

    if "zee" in content:
        await message.delete()
        await message.channel.send(f"{message.author.mention} - wag mo banggitin yan!")

    await bot.process_commands(message)

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}!")

# ===== STATUS COMMANDS =====
@bot.command()
async def lil(ctx, *, status: str = None):
    global lil_status
    ALLOWED_USER_ID = 625311802703740968  # Lil's ID

    if status is None:
        if lil_status:
            await ctx.send(f"📢 Lil is currently **{lil_status}**!")
        else:
            await ctx.send("Lil status has not been set yet.")
    else:
        if ctx.author.id != ALLOWED_USER_ID:
            await ctx.send("❌ You are not allowed to change Lil's status.")
            return

        lil_status = status
        save_status(LIL_STATUS_FILE, lil_status)
        await ctx.send(f"✅ Lil's status has been set to **{status}**!")

@bot.command()
async def sav(ctx, *, status: str = None):
    global sav_status
    ALLOWED_USER_ID = 734792664767266957  # Sav's ID

    if status is None:
        if sav_status:
            await ctx.send(f"😡 Sav is currently **{sav_status}**!")
        else:
            await ctx.send("Sav status has not been set yet.")
    else:
        if ctx.author.id != ALLOWED_USER_ID:
            await ctx.send("❌ You are not allowed to change Sav's status.")
            return

        sav_status = status
        save_status(SAV_STATUS_FILE, sav_status)
        await ctx.send(f"✅ Sav's status has been set to **{status}**!")

@bot.command()
async def yuks(ctx, *, status: str = None):
    global yuks_status
    ALLOWED_USER_ID = 1280132085616738387  # Yuks' ID

    if status is None:
        if yuks_status:
            await ctx.send(f"😏 Yuks is currently **{yuks_status}**!")
        else:
            await ctx.send("Yuks status has not been set yet.")
    else:
        if ctx.author.id != ALLOWED_USER_ID:
            await ctx.send("❌ You are not allowed to change Yuks' status.")
            return

        yuks_status = status
        save_status(YUKS_STATUS_FILE, yuks_status)
        await ctx.send(f"✅ Yuks' status has been set to **{status}**!")


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
    await ctx.reply("!hello, !lil, !sav, !yuks, !tiktok, !rank, !aiz")

@bot.command()
async def poll(ctx, *, question):
    target_channel_id = 1407904625969074216
    target_channel = bot.get_channel(target_channel_id)

    if not target_channel:
        await ctx.send("❌ Couldn't find the target poll channel.")
        return

    embed = discord.Embed(
        title="📢 **THOUGHTS NI LIL – CAST YOUR VOTE!**",
        description=(
            f"**⬇️ QUESTION:**\n"
            f"__{question}__\n\n"
            f"👍 = Agree\n"
            f"👎 = Disagree\n"
            f"🤔 = Neutral / Thinking\n\n"
            f"🗳️ React below to vote!"
        ),
        color=random.choice([
            discord.Color.green(),
            discord.Color.blue(),
            discord.Color.purple(),
            discord.Color.gold()
        ]),
        timestamp=ctx.message.created_at
    )

    embed.set_thumbnail(url="https://i.pinimg.com/736x/5c/dd/8d/5cdd8d89ce9d32e38f97c50ccece9933.jpg")
    embed.set_footer(
        text="📝 Powered by Lil bot • Made by aiz",
        icon_url=ctx.guild.icon.url if ctx.guild.icon else discord.Embed.Empty
    )

    poll_message = await target_channel.send(embed=embed)
    await poll_message.add_reaction("👍")
    await poll_message.add_reaction("👎")
    await poll_message.add_reaction("🤔")

    await ctx.send(f"✅ Your poll has been posted in {target_channel.mention}!")


@bot.command()
async def tiktoklive(ctx):
    target_channel_id = 1413683705876316241
    channel = bot.get_channel(target_channel_id)

    if channel is not None:
        embed = discord.Embed(
            title="🔴 lil ₍^. .^₎⟆ is LIVE on TikTok!",
            description=(
                "🎥 **lil ₍^. .^₎⟆** just went live on TikTok!\n\n"
                "✨ Come chill, vibe, and be part of the stream — it’s gonna be a fun time you won’t want to miss.\n\n"
                "👉 **Tap below to join the live now:**\n"
                "[📲 Watch the Stream](https://www.tiktok.com/@shanghaispicy)"
            ),
            color=discord.Color.from_rgb(255, 0, 102),
            timestamp=ctx.message.created_at
        )

        embed.set_thumbnail(url="https://p16-sign-sg.tiktokcdn.com/tos-alisg-avt-0068/428c7dae719755755d2ef225baaf33b5~tplv-tiktokx-cropcenter:1080:1080.jpeg?dr=14579&refresh_token=b3fc6615&x-expires=1757289600&x-signature=WDhDpHPqL%2BLOa0gj%2FixUgRo3x3c%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my")
        embed.set_image(url="https://i.pinimg.com/originals/82/14/dc/8214dc94282b4037f65747e130ca6c70.gif")

        embed.set_footer(
            text="🔗 Powered by Lil bot • Brought to you by aiz",
            icon_url=ctx.guild.icon.url if ctx.guild.icon else discord.Embed.Empty
        )

        await channel.send(content="@everyone", embed=embed)
        await ctx.send("✅ Live alert sent!")
    else:
        await ctx.send("❌ Could not find the live announcement channel.")

@bot.command()
async def kiss(ctx, member: discord.Member = None):
    if not member:
        await ctx.send("You need to mention someone to kiss! 😳")
        return
    if member == ctx.author:
        await ctx.send("Awww, self-love is important! 😘")
        return
    gif = await fetch_giphy_gif("anime kiss")
    if not gif:
        await ctx.send("Couldn't fetch a kiss GIF right now, try again later!")
        return
    embed = discord.Embed(description=f"💋 {ctx.author.mention} kisses {member.mention}!", color=discord.Color.pink())
    embed.set_image(url=gif)
    await ctx.send(embed=embed)

@bot.command()
async def slap(ctx, member: discord.Member = None):
    if not member:
        await ctx.send("Mention someone to slap! 😡")
        return
    if member == ctx.author:
        await ctx.send("Why are you slapping yourself? 😢")
        return
    gif = await fetch_giphy_gif("anime slap")
    if not gif:
        await ctx.send("Couldn't fetch a slap GIF right now, try again later!")
        return
    embed = discord.Embed(description=f"👋 {ctx.author.mention} slaps {member.mention}!", color=discord.Color.red())
    embed.set_image(url=gif)
    await ctx.send(embed=embed)

@bot.command()
async def hug(ctx, member: discord.Member = None):
    if not member:
        await ctx.send("You gotta mention someone to hug! 🤗")
        return
    if member == ctx.author:
        await ctx.send("Sending a virtual hug to yourself 🤗💖")
        return
    gif = await fetch_giphy_gif("anime hug")
    if not gif:
        await ctx.send("Couldn't fetch a hug GIF right now, try again later!")
        return
    embed = discord.Embed(description=f"🤗 {ctx.author.mention} gives {member.mention} a warm hug!", color=discord.Color.blue())
    embed.set_image(url=gif)
    await ctx.send(embed=embed)

@bot.command()
async def punch(ctx, member: discord.Member = None):
    """Playful, non-graphic punch (like slap)."""
    if not member:
        await ctx.send("Mention someone to punch! (playfully) 🥊")
        return
    if member == ctx.author:
        await ctx.send("Why are you punching yourself? Be kind to yourself! 🤕")
        return
    gif = await fetch_giphy_gif("anime punch")
    if not gif:
        await ctx.send("Couldn't fetch a punch GIF right now, try again later!")
        return
    embed = discord.Embed(description=f"🥊 {ctx.author.mention} playfully punches {member.mention}!", color=discord.Color(0xE53935))
    embed.set_image(url=gif)
    await ctx.send(embed=embed)

@bot.command()
async def kill(ctx, member: discord.Member = None):
    """Cute boop command — PG friendly."""
    if not member:
        await ctx.send("Who do you want to kill? Mention someone! 👀")
        return
    if member == ctx.author:
        await ctx.send("Killing yourself? A+ self-harm. 🤗")
        return
    gif = await fetch_giphy_gif("kill anime")
    if not gif:
        await ctx.send("Couldn't fetch a kill GIF right now, try again later!")
        return
    embed = discord.Embed(description=f"👆 {ctx.author.mention} gives {member.mention} a finishing blow!", color=discord.Color.blue())
    embed.set_image(url=gif)
    await ctx.send(embed=embed)

@bot.command()
async def vanish(ctx, member: discord.Member = None):
    """Playful 'vanish' — harmless alternative to destructive commands."""
    target_text = f" at {member.mention}" if member and member != ctx.author else ""
    if member == ctx.author:
        await ctx.send("You try to vanish... but you're still here. ✨")
        return
    gif = await fetch_giphy_gif("poof disappear anime")
    if not gif:
        await ctx.send(f"{ctx.author.mention} dramatically vanishes{target_text}... (but comes back soon).")
        return
    embed = discord.Embed(description=f"✨ {ctx.author.mention} dramatically vanishes{target_text}... (it's just a prank!)", color=discord.Color.purple())
    embed.set_image(url=gif)
    await ctx.send(embed=embed)

@bot.command()
async def wyr(ctx):
    """Edgy Tagalog Would You Rather game"""
    questions = [
        # Life struggles
        ("Mawala net mo habang ranked 🔌", "Mawala kuryente habang live ⚡"),
        ("Maging single forever 💔", "Maging taken pero toxic 😬"),
        ("Di ka na makakain ng Jollibee 🍗", "Di ka na makakain ng Mang Inasal 🍴"),
        ("Maging pogi/ganda pero bobo 😅", "Maging matalino pero walang jowa 📖"),
        ("Laging late pero pogi/ganda ⏰", "Laging on time pero baduy 😬"),
        ("Maging mayaman pero pangit 💸", "Maging maganda/pogi pero broke 💔"),
        ("Laging galet si sav 😡", "Laging clingy si aiz 🥴"),

        # Gaming
        ("Maging Radiant sa Valorant 🎯", "Maging Challenger sa LoL 🧙‍♂️"),
        ("Magpuyat sa ML hanggang 6AM 📱", "Mag-all nighter sa thesis 📚"),
        ("Magka-ace sa Valorant 💥", "Mag-pentakill sa LoL 🔥"),
        ("Talo lagi sa ranked 😭", "AFK lagi teammate mo 😡"),

        # School/Work
        ("Walang kape habang exam ☕", "Walang tulog habang exam 😵"),
        ("Mag-report sa harap ng class 📢", "Mag-sayaw sa TikTok sa harap ng lahat 💃"),
        ("Maging cum laude pero walang friends 🎓", "Maging happy-go-lucky pero bagsak lagi 😅"),
        ("Laging gutom sa school 🍜", "Laging broke sa school 💸"),

        # Daily life
        ("Sumakay ng jeep na siksikan 🚌", "Sumakay ng MRT na amoy pawis 🚇"),
        ("Sumabay sa bagyo 🌪️", "Sumabay sa baha 🌊"),
        ("Maglakad sa ulan 🌧️", "Maglakad sa init ng araw ☀️"),
        ("Laging lowbat 🔋", "Laging walang load 📶"),

        # Relationships / Spicy (but safe)
        ("Maging loyal pero laging busy 📵", "Maging sweet pero seloso/selosa 😏"),
        ("Makita ex mo araw-araw 👀", "Maging classmate ang ex mo buong semester 📚"),
        ("Maging marupok 💔", "Maging manhid 🥶"),
        ("Ghosted 👻", "Zinonezone ☝️"),
    ]

    option1, option2 = random.choice(questions)

    embed = discord.Embed(
        title="🤔 Would You Rather (Pinoy Edition)",
        description=f"1️⃣ {option1}\n\n2️⃣ {option2}\n\nReact ka na!",
        color=discord.Color.random(),
        timestamp=ctx.message.created_at
    )
    embed.set_footer(text="📝 Powered by Lil bot • Edgy Tagalog WYR")

    wyr_message = await ctx.send(embed=embed)

    # Reactions for voting
    await wyr_message.add_reaction("1️⃣")
    await wyr_message.add_reaction("2️⃣")

@bot.command()
async def vct(ctx, mode: str = "upcoming"):
    """
    Fetches VCT match info using vlrggapi.
    Usage: !vct upcoming | live | results
    """

    mode_map = {
        "upcoming": "upcoming",
        "live": "live_score",
        "results": "results"
    }

    if mode.lower() not in mode_map:
        await ctx.send("❌ Invalid mode! Use one of: `!vct upcoming`, `!vct live`, `!vct results`")
        return

    q = mode_map[mode.lower()]
    url = f"https://vlrggapi.vercel.app/match?q={q}"

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=10) as resp:
                text = await resp.text()
                print(f"[VCT Debug] GET {url} → Status: {resp.status}, Body starts with: {text[:200]}")

                # Handle "no matches" response (404 or empty JSON)
                if resp.status == 404:
                    await ctx.send(f"ℹ️ No {mode} matches found right now.")
                    return
                if resp.status != 200:
                    await ctx.send(f"⚠️ API error (status {resp.status}). Try again later.")
                    return

                data = await resp.json()
        except Exception as e:
            await ctx.send("⚠️ Error fetching match data: " + str(e))
            return

    segments = data.get("data", {}).get("segments", [])
    if not segments:
        await ctx.send(f"ℹ️ No {mode} matches found right now.")
        return

    for seg in segments[:3]:
        team1 = seg.get("team1", "TBD")
        team2 = seg.get("team2", "TBD")
        series = seg.get("match_series", "")
        event = seg.get("match_event", "")
        time_until = seg.get("time_until_match", "") or seg.get("unix_timestamp", "")
        match_page = seg.get("match_page", "")

        embed = discord.Embed(
            title=f"{event} • {series}",
            description=f"**{team1} vs {team2}**\n🕒 {time_until}",
            color=discord.Color.green() if mode.lower() == "live" else discord.Color.blue()
        )
        if match_page:
            embed.add_field(name="Match Page", value=f"[Click here to view]({match_page})", inline=False)
        embed.set_footer(text=f"Mode: {mode.title()} • Powered by vlr.gg API")

        await ctx.send(embed=embed)

# Run bot
bot.run(token, log_handler=handler, log_level=logging.INFO)



