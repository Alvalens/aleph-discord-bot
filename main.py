# import discord
import asyncio
import interactions
from dotenv import load_dotenv
import os

from image_search import task, get_image_url
from interactions import (
    Client,
    slash_command,
    SlashContext,
    Intents,
    listen,
    slash_option,
    Button,
    ButtonStyle,
)
from interactions.api.events import Component, MessageCreate

load_dotenv()


# Get the Discord bot token from the environment variables
# token = os.getenv("token")
client = Client(
    token=os.environ.get("TOKEN"),
    intents=Intents.ALL,
    
)

# listener whenever someone sends a message containing 'aleph'
@listen(MessageCreate)
async def on_message_create(event: MessageCreate):
    if event.message.author.bot:
        return
    # if aleph, hi, hello, hay, hey or helo in the message
    if "aleph" in event.message.content.lower() or "hi" in event.message.content.lower() or "hello" in event.message.content.lower() or "hay" in event.message.content.lower() or "hey" in event.message.content.lower() or "helo" in event.message.content.lower():
        await event.message.reply(f"Hello {event.message.author.mention}! How can I help you today? 😊")
        
@listen()
async def on_ready():
    print("Bot is ready")
    await client.change_presence(
        status=interactions.Status.IDLE,
        activity=interactions.Activity(
            type=interactions.ActivityType.PLAYING, name="Hello, I'm Aleph!"
        ),
    )
    

# Command to display the list of available commands
@slash_command(name="help", description="Displays a list of commands")
async def help(ctx: SlashContext):
    embed = interactions.Embed(title="Commands", color=0x00FF00)
    embed.add_field(
        name="image", value=f"Searches for an image ex: /image keywords", inline=False
    )
    embed.add_field(name="ping", value="Pings the bot ex: /ping", inline=False)
    embed.add_field(
        name="clear",
        value="Deletes the specified number of messages ex: /clear 5",
        inline=False,
    )
    await ctx.defer()
    await ctx.send(embed=embed)


# # Command to ping the bot
@slash_command(name="ping", description="Pings the bot")
async def ping(ctx: SlashContext):
    await ctx.send("Pong!")


# Command to search for an image
@slash_command(name="image", description="Searches for an image")
@slash_option(
    name="keyword",
    description="The keyword to search for",
    required=True,
    opt_type=interactions.OptionType.STRING,
)
async def image(ctx: SlashContext, keyword: str):
    try:
        if not keyword:
            await ctx.send("Please enter a keyword!")
            raise ValueError("Please enter a keyword!")

        await ctx.send("Searching for images...")
        image_urls = await task(keyword)
        if image_urls:
            # embed
            embed = interactions.Embed(title=keyword, color=0x00FF00)
            rand_url = get_image_url(image_urls)
            embed.set_image(url=rand_url)
            # message = await ctx.send(embed=embed)

            button = Button(
                
                style=ButtonStyle.PRIMARY,
                label="Change Image"
            )

            # Add the button to the message
            message = await ctx.send(embed=embed, components=[button])

            # Change the image
            while True:
                try:
                    used_component: Component = await client.wait_for_component(components=button, timeout=30)

                    await used_component.ctx.defer(edit_origin=True)
                    rand_url = get_image_url(image_urls)
                    embed.set_image(url=rand_url)
                    await message.edit(embed=embed)
                    await used_component.ctx.edit_origin(
                        embed=embed, content="Image changed!"
                    )
                except asyncio.TimeoutError:
                    print("Timeout")
                    button.disabled = True
                    await message.edit(components=button)
                    break
                except Exception as e:
                    print(f"Error making API request: {e}")
                    raise ValueError("Error making API request")
        else:
            await ctx.send(f"No images found for '{keyword}'")

    except ValueError as e:
        await ctx.send(str(e))


# Command to delete messages
@slash_command(name="clear", description="Deletes messages")
@slash_option(
    name="amount",
    description="The number of messages to delete",
    required=True,
    opt_type=interactions.OptionType.INTEGER,
)
async def clear(ctx: SlashContext, amount: int = 5):
    await ctx.channel.purge(deletion_limit = amount + 1)
    await ctx.send(f"Deleted {amount} messages")
    await asyncio.sleep(3)
    await ctx.delete()

# Start the bot
client.start()
