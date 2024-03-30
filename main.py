import os

from dotenv import load_dotenv

from src.bot import client

load_dotenv()
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

if __name__ == "__main__":
    client.run(DISCORD_BOT_TOKEN)
