# Aleph Bot
![visitor badge](https://visitor-badge.laobi.icu/badge?page_id=alvalens.visitor-badge)

Aleph Bot is a Discord bot that allows you to search for images based on keywords and some other utility commands.

[![AlephZe](https://dcbadge.vercel.app/api/server/cZH93kM)](https://discord.gg/cZH93kM) ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Discord](https://img.shields.io/badge/Discord-%235865F2.svg?style=for-the-badge&logo=discord&logoColor=white)

## Features

- Image search: Search for images based on keywords using the `?image` command.

## Installation

1. Clone the repository:

   ```git
   git clone git@github.com:Alvalens/discord-bot.git
   ```

2. Install the required dependencies:
3. Create a `.env` or copy the .env.example file in the project root with the following content:

   ```
   token=YOUR_DISCORD_BOT_TOKEN
   login=YOUR_API_LOGIN
   password=YOUR_API_PASSWORD
   ```

   Replace `token`, `login`, and `paddword` with your actual tokens and credentials. SERP API used: [DataForSeo Google image search](https://dataforseo.com/)
4. Run the bot

   ```python
   py main.py
   ```

## Usage

* `?image<keywords>`: Searches for images based on the provided keywords.
* `?help`: Show avalible commands
* `?ping`: Pings the bot and returns "Pong!".

## Contributing

Contributions are welcome! If you find any issues or have suggestions, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License seethe [LICENSE](LICENSE) file for details.
