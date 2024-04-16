import os

from dotenv import load_dotenv

from avocado import bot

load_dotenv()
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

if __name__ == "__main__":
    bot.run(DISCORD_BOT_TOKEN)
