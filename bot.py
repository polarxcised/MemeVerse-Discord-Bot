import os
import discord
import random
import requests
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GIPHY_API_KEY = os.getenv("GIPHY_API_KEY")

# API URLs
APIS = {
    "JOKE": "https://v2.jokeapi.dev/joke/Any",
    "INSULT": "https://evilinsult.com/generate_insult.php?lang=en&type=json",
    "CHUCK_NORRIS": "https://api.chucknorris.io/jokes/random",
    "RICKMORTY_CHAR": "https://rickandmortyapi.com/api/character",
    "RICKMORTY_LOC": "https://rickandmortyapi.com/api/location",
    "WEATHER": "https://www.7timer.info/bin/astro.php?lon={lon}&lat={lat}&unit=metric&output=json",
    "FACTS": "https://uselessfacts.jsph.pl/random.json?language=en",
    "ADVICE": "https://api.adviceslip.com/advice",
    "GIPHY": "https://api.giphy.com/v1/gifs/random",
}

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Function to fetch data
def fetch_api(url, params=None):
    try:
        response = requests.get(url, params=params)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# --- Commands per API ---
# Joke API
@bot.command()
async def joke(ctx):
    """!joke - Get a random joke."""
    data = fetch_api(APIS["JOKE"])
    if "joke" in data:
        await ctx.send(data['joke'])
    elif "setup" in data and "delivery" in data:
        await ctx.send(f"{data['setup']}\n{data['delivery']}")
    else:
        await ctx.send("Couldn't fetch a joke.")

@bot.command()
async def jokeprogramming(ctx):
    """!jokeprogramming - Get a programming joke."""
    data = fetch_api(f"{APIS['JOKE']}?type=twopart&category=Programming")
    if "setup" in data and "delivery" in data:
        await ctx.send(f"{data['setup']}\n{data['delivery']}")
    else:
        await ctx.send("Couldn't fetch a programming joke.")

@bot.command()
async def jokegeneral(ctx):
    """!jokegeneral - Get a general joke."""
    data = fetch_api(f"{APIS['JOKE']}?type=twopart&category=General")
    if "setup" in data and "delivery" in data:
        await ctx.send(f"{data['setup']}\n{data['delivery']}")
    else:
        await ctx.send("Couldn't fetch a general joke.")

# Insult API
@bot.command()
async def insult(ctx):
    """!insult - Get a random insult."""
    data = fetch_api(APIS["INSULT"])
    await ctx.send(data.get("insult", "No insults for now!"))

@bot.command()
async def insultuser(ctx, user: discord.Member):
    """!insultuser <user> - Send an insult to a user."""
    data = fetch_api(APIS["INSULT"])
    await ctx.send(f"{user.mention}, {data.get('insult', 'No insult for now!')}")

@bot.command()
async def insultrandom(ctx):
    """!insultrandom - Random insult without a target."""
    data = fetch_api(APIS["INSULT"])
    await ctx.send(data.get("insult", "Couldn't fetch an insult."))

# Chuck Norris API
@bot.command()
async def chuck(ctx):
    """!chuck - Get a random Chuck Norris joke."""
    data = fetch_api(APIS["CHUCK_NORRIS"])
    await ctx.send(data["value"])

@bot.command()
async def chuckfact(ctx):
    """!chuckfact - Get a Chuck Norris fact."""
    data = fetch_api(APIS["CHUCK_NORRIS"])
    await ctx.send(f"💪 **Chuck Norris Fact:** {data['value']}")

@bot.command()
async def chuckjoke(ctx):
    """!chuckjoke - Another Chuck Norris joke."""
    data = fetch_api(APIS["CHUCK_NORRIS"])
    await ctx.send(data["value"])

# Rick and Morty API
@bot.command()
async def rickchar(ctx):
    """!rickchar - Get a random Rick and Morty character."""
    data = fetch_api(APIS["RICKMORTY_CHAR"])
    char = random.choice(data['results'])
    await ctx.send(f"🪐 **Character**: {char['name']}\nStatus: {char['status']}")

@bot.command()
async def rickloc(ctx):
    """!rickloc - Get a random Rick and Morty location."""
    data = fetch_api(APIS["RICKMORTY_LOC"])
    loc = random.choice(data['results'])
    await ctx.send(f"🌌 **Location**: {loc['name']}, Type: {loc['type']}")

@bot.command()
async def rickstats(ctx):
    """!rickstats - Rick and Morty character stats."""
    data = fetch_api(APIS["RICKMORTY_CHAR"])
    total_chars = data.get('info', {}).get('count', 'Unknown')
    await ctx.send(f"📊 **Total Rick and Morty Characters:** {total_chars}")

# Weather API
@bot.command()
async def weather(ctx, lat: float, lon: float):
    """!weather <lat> <lon> - Get the weather for a location."""
    data = fetch_api(APIS["WEATHER"].format(lat=lat, lon=lon))
    temp = data['dataseries'][0]['temp2m']
    await ctx.send(f"🌤️ **Weather:** {temp}°C at {lat}, {lon}")

@bot.command()
async def astro(ctx, lat: float, lon: float):
    """!astro <lat> <lon> - Astronomical weather data."""
    data = fetch_api(APIS["WEATHER"].format(lat=lat, lon=lon))
    seeing = data['dataseries'][0]['seeing']
    await ctx.send(f"🔭 **Astronomical Seeing:** {seeing} (lower is better)")

@bot.command()
async def cloudcover(ctx, lat: float, lon: float):
    """!cloudcover <lat> <lon> - Cloud cover percentage."""
    data = fetch_api(APIS["WEATHER"].format(lat=lat, lon=lon))
    cloud = data['dataseries'][0]['cloudcover']
    await ctx.send(f"☁️ **Cloud Cover:** {cloud}% at {lat}, {lon}")

# Facts API
@bot.command()
async def randomfact(ctx):
    """!randomfact - Get a random fact."""
    data = fetch_api(APIS["FACTS"])
    await ctx.send(f"💡 **Did You Know?** {data['text']}")

@bot.command()
async def funfact(ctx):
    """!funfact - Another random fact."""
    data = fetch_api(APIS["FACTS"])
    await ctx.send(f"💡 **Fact:** {data['text']}")

@bot.command()
async def uselessfact(ctx):
    """!uselessfact - Useless random fact."""
    data = fetch_api(APIS["FACTS"])
    await ctx.send(f"🤔 **Useless Fact:** {data['text']}")

# Advice API
@bot.command()
async def advice(ctx):
    """!advice - Random advice."""
    data = fetch_api(APIS["ADVICE"])
    await ctx.send(f"🧠 **Advice:** {data['slip']['advice']}")

@bot.command()
async def advicefortoday(ctx):
    """!advicefortoday - Inspirational advice."""
    data = fetch_api(APIS["ADVICE"])
    await ctx.send(f"🌟 **Advice for Today:** {data['slip']['advice']}")

@bot.command()
async def randomadvice(ctx):
    """!randomadvice - Get random advice."""
    data = fetch_api(APIS["ADVICE"])
    await ctx.send(f"💡 **Random Advice:** {data['slip']['advice']}")

# GIF API
@bot.command()
async def gif(ctx, tag="funny"):
    """!gif [tag] - Fetch a random GIF based on a tag."""
    params = {"api_key": GIPHY_API_KEY, "tag": tag}
    data = fetch_api(APIS["GIPHY"], params=params)
    gif_url = data.get("data", {}).get("images", {}).get("original", {}).get("url")
    if gif_url:
        await ctx.send(f"🎥 **Here's a `{tag}` GIF:** {gif_url}")
    else:
        await ctx.send(f"Couldn't fetch a `{tag}` GIF.")

@bot.command()
async def gifrandom(ctx):
    """!gifrandom - Fetch a random GIF."""
    params = {"api_key": GIPHY_API_KEY}
    data = fetch_api(APIS["GIPHY"], params=params)
    gif_url = data.get("data", {}).get("images", {}).get("original", {}).get("url")
    if gif_url:
        await ctx.send(f"🎥 **Random GIF:** {gif_url}")
    else:
        await ctx.send("Couldn't fetch a random GIF.")

@bot.command()
async def giftrending(ctx):
    """!giftrending - Fetch a trending GIF."""
    params = {"api_key": GIPHY_API_KEY, "tag": "trending"}
    data = fetch_api(APIS["GIPHY"], params=params)
    gif_url = data.get("data", {}).get("images", {}).get("original", {}).get("url")
    if gif_url:
        await ctx.send(f"🔥 **Trending GIF:** {gif_url}")
    else:
        await ctx.send("Couldn't fetch a trending GIF.")

# --- Enhanced !what Command ---
@bot.command()
async def what(ctx):
    """!what - List of commands."""
    embed = discord.Embed(title="📋 **List of Commands**", description="Use these commands to interact with the bot!", color=discord.Color.blue())
    
    embed.add_field(name="🎥 **GIF Commands**", value="""
    `!gif [tag]` - Fetch a random GIF by tag.  
    `!gifrandom` - Fetch a completely random GIF.  
    `!giftrending` - Fetch a trending GIF.  
    """, inline=False)
    
    embed.add_field(name="🎉 **Fun Commands**", value="""
    `!joke`, `!jokeprogramming`, `!jokegeneral` - Jokes.  
    `!randomfact`, `!funfact`, `!uselessfact` - Facts.  
    """, inline=False)
    
    embed.add_field(name="🎤 **Insult Commands**", value="""
    `!insult`, `!insultuser <user>`, `!insultrandom` - Insults.  
    """, inline=False)

    embed.add_field(name="🌤️ **Weather Commands**", value="""
    `!weather`, `!astro`, `!cloudcover` - Weather data.  
    """, inline=False)
    
    embed.set_footer(text="Made by polarxcised | Enjoy using the bot! 🚀")
    await ctx.send(embed=embed)

# Run the bot
bot.run(DISCORD_TOKEN)
