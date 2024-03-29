from bot.main_bot import CasuBot 
from discord import Intents

from dotenv import load_dotenv
import os
load_dotenv()

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")

def main() -> None:
    commandPrefix = "c!"
    description = "test"
    intents = Intents.all()
    helpCommand = None

    bot = CasuBot(command_prefix = commandPrefix, description = description, intents = intents, help_command = helpCommand)
    bot.setup()
    bot.run(DISCORD_TOKEN)

if __name__ == "__main__":
    main()