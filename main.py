# import discord
import asyncio
import random
import interactions
from dotenv import load_dotenv
import os

from image_search import task, get_image_url
from gemini import call_model
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

async def fetch_last_messages(channel, limit=10):
    messages = await channel.history(limit=limit).flatten()
    return [message.content for message in messages]


# listener whenever someone sends a message containing 'aleph'
@listen(MessageCreate)
async def on_message_create(event: MessageCreate):
    """
    Listens for new messages and responds with a greeting if certain keywords are detected.

    Args:
        event (MessageCreate): The event object representing the newly created message.

    Returns:
        None
    """
    if event.message.author.bot:
        return
    # if aleph, hi, hello, hay, hey or helo in the message
    if "aleph" in event.message.content.lower() or "hi" in event.message.content.lower() or "hello" in event.message.content.lower() or "hay" in event.message.content.lower() or "hey" in event.message.content.lower() or "helo" in event.message.content.lower():
        await event.message.reply(f"Hello {event.message.author.mention}! How can I help you today? 😊")


@listen()
async def on_ready():
    """
    Event handler for when the bot is ready.

    This function is called when the bot has successfully connected to the Discord server and is ready to start receiving events.

    It prints a message to indicate that the bot is ready and sets the bot's presence to show that it is idle and playing a game.

    Parameters:
        None

    Returns:
        None
    """
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
    """
    Displays a list of commands.

    Parameters:
    - ctx (SlashContext): The context of the slash command.

    Returns:
    - None

    Example usage:
    /help
    """
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

# command to check current month bational day of indonesia
@slash_command(name="libur", description="Check the national day of Indonesia")
@slash_option(
    name="month",
    description="The month to check",
    required=True,
    opt_type=interactions.OptionType.INTEGER,
)
async def libur(ctx: SlashContext, month: int):
    """
    Check the national day of Indonesia for the specified month.

    Parameters:
    - ctx (SlashContext): The context of the slash command.
    - month (int): The month to check.

    Returns:
    None
    """
    try:
        if month < 1 or month > 12:
            await ctx.send("Invalid month! Please enter a month between 1 and 12.")
            raise ValueError("Invalid month! Please enter a month between 1 and 12.")

        await ctx.send(f"Checking national day for month {month}...")
        response = await client.get_async(f"/api?month={month}")
        if response:
            holidays = response
            if holidays:
                for holiday in holidays:
                    if holiday["is_national_holiday"]:
                        await ctx.send(f"{holiday['holiday_date']}: {holiday['holiday_name']}")
            else:
                await ctx.send("No national holidays found for the specified month.")
        else:
            await ctx.send("No data found for the specified month.")

    except ValueError as e:
        await ctx.send()
    except Exception as e:
        print(f"Error making API request: {e}")
        raise ValueError("Error making API request")


# Command to ping the bot
@slash_command(name="ping", description="Pings the bot")
async def ping(ctx: SlashContext):
    """
    Sends a ping message to the bot.

    Parameters:
    - ctx (SlashContext): The context of the slash command.

    Returns:
    - None
    """
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
    """
    Searches for an image based on the provided keyword and displays it in an embed.
    
    Parameters:
    - ctx (SlashContext): The context of the slash command.
    - keyword (str): The keyword to search for.
    
    Raises:
    - ValueError: If no keyword is provided.
    - ValueError: If there is an error making the API request.
    
    Returns:
    - None
    """
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
                    # print(f"Error making API request: {e}")
                    ctx.send("Error making API request")
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
    """
    Clears a specified number of messages in the channel.

    Parameters:
    - ctx (SlashContext): The context of the slash command.
    - amount (int): The number of messages to delete. Default is 5.

    Returns:
    None
    """
    await ctx.channel.purge(deletion_limit=amount + 1)
    await ctx.send(f"Deleted {amount} messages")
    await asyncio.sleep(3)
    await ctx.delete()

# command take a list of string to gacha pick one random string
@slash_command(name="gacha", description="Pick a random string from the list")
@slash_option(
    name="list",
    description="List of strings separated by comma",
    required=True,
    opt_type=interactions.OptionType.STRING,
)
async def gacha(ctx: SlashContext, list: str):
    """
    Pick a random string from the list of strings provided by the user.

    Parameters:
    - ctx (SlashContext): The context of the slash command.
    - list (str): List of strings separated by comma.

    Returns:
    None
    """
    try:
        if not list:
            await ctx.send("Please enter a list of strings separated by comma!")
            raise ValueError("Please enter a list of strings separated by comma!")

        list = list.split(",")
        rand_str = list[random.randint(0, len(list) - 1)]
        await ctx.send(f"Randomly picked: {rand_str}")

    except ValueError as e:
        await ctx.send(str(e))

@slash_command(name="ask", description="Ask a question")
@slash_option(
    name="question",
    description="The question to ask",
    required=True,
    opt_type=interactions.OptionType.STRING,
)
async def ask(ctx: SlashContext, question: str):
    """
    Ask a question and get a response from the chatbot.

    Parameters:
    - ctx (SlashContext): The context of the slash command.
    - question (str): The question to ask.

    Returns:
    None
    """
    user_name = ctx.author.username
    channel = ctx.channel
    try:
        if not question:
            await ctx.send("Please enter a question!")
            raise ValueError("Please enter a question!")

        context = await fetch_last_messages(channel, limit=10)
        initial_message = await ctx.send("Asking the bot...")
        response = call_model(user_name, question, context)
        await initial_message.edit(content=response)

    except ValueError as e:
        await ctx.send(str(e))


# Start the bot
client.start()
