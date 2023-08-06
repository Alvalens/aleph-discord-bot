import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from image_search import task

intents = discord.Intents.default()
intents.typing = True
intents.presences = False
intents.message_content = True

bot = commands.Bot(command_prefix=('?'), intents=intents)

bot.remove_command('help')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
@bot.command(name='help', hidden=False)
async def help(ctx):
    # command list
    embed = discord.Embed(title="Commands", color=0x00ff00)
    embed.add_field(name="image", value="Searches for an image", inline=False)
    embed.add_field(name="ping", value="Pings the bot", inline=False)
    await ctx.send(embed=embed)
@bot.command(name='ping', hidden=False)
async def ping(ctx):
    await ctx.send("Pong!")
@bot.command()
async def image(ctx, *, keyword):
    try:
        if not keyword:
            await ctx.send("Please enter a keyword!")
            raise ValueError("Please enter a keyword!")

        await ctx.send("Searching for images...")
        image_url = task(keyword)

        if image_url:
            # embed
            embed = discord.Embed(title=keyword, color=0x00ff00)
            embed.set_image(url=image_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"No images found for '{keyword}'")

        await ctx.send("Done!")

    except ValueError as e:
        await ctx.send(str(e))


# Replace "YOUR_DISCORD_BOT_TOKEN" with your actual Discord bot token
load_dotenv()
bot.run(os.getenv("token"))
