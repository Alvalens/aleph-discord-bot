import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from image_search import task, get_image_url
import asyncio


# token
load_dotenv()
token = os.getenv("token")

intents = discord.Intents.default()
intents.typing = True
intents.presences = False
intents.message_content = True

bot = commands.Bot(command_prefix=('?'), intents=intents)

bot.remove_command('help')


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    await bot.change_presence(status=discord.Status.idle)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="Hello, I'm a bot!"))


@bot.command(name='help', hidden=False)
async def help(ctx):
    # command list
    embed = discord.Embed(title="Commands", color=0x00ff00)
    embed.add_field(
        name="image", value=f"Searches for an image ex: ?images keywords", inline=False)
    embed.add_field(name="ping", value="Pings the bot ex: ?ping", inline=False)
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
        image_urls = await task(keyword)

        if image_urls:
            # embed
            embed = discord.Embed(title=keyword, color=0x00ff00)
            rand_url = get_image_url(image_urls)
            embed.set_image(url=rand_url)
            message = await ctx.send(embed=embed)

            # add reaction to embed
            await message.add_reaction("🔄")

            # reaction to change image
            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) == '🔄'

            while True:
                try:
                    reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check)
                    if str(reaction.emoji) == '🔄':
                        rand_url = get_image_url(image_urls)
                        embed.set_image(url=rand_url)
                        await message.edit(embed=embed)
                        await reaction.remove(user)
                except asyncio.TimeoutError:
                    await ctx.send("Timed out!")
                    break

        else:
            await ctx.send(f"No images found for '{keyword}'")

    except ValueError as e:
        await ctx.send(str(e))

# add button in rich presence


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content == "Hello" or message.content == "hello" or message.content == "hi" or message.content == "Hi" or message.content == "hey" or message.content == "Hey" or message.content == "halo" or message.content == "Halo" or message.content == "Hai" or message.content == "hai":
        await message.channel.send(f"Hello {message.author.mention} 👋")
    await bot.process_commands(message)

# utility commands to delete messages


@bot.command(name='clear', hidden=False)
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f"{amount} messages deleted!")
    await asyncio.sleep(2)
    await ctx.channel.purge(limit=1)


# Replace "YOUR_DISCORD_BOT_TOKEN" with your actual Discord bot token
bot.run(token)
