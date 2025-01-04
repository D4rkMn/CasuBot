from bot.main_bot import CasuBot 
from discord import Intents

from dotenv import load_dotenv
import os
load_dotenv()

# Get if debug mode
DEBUG_MODE = os.getenv("DEBUG", "false").lower() == "true"

# If not debug then run casu. Else, run dorito
if not DEBUG_MODE:
    DISCORD_TOKEN = os.environ.get("CASU_TOKEN")
    COMMAND_PREFIX = "c!"
else:
    DISCORD_TOKEN = os.environ.get("DORITO_TOKEN")
    COMMAND_PREFIX = "d!"

def main() -> None:
    description = "test"
    intents = Intents.all()
    helpCommand = None

    bot = CasuBot(command_prefix = COMMAND_PREFIX, description = description, intents = intents, help_command = helpCommand)
    bot.setup()
    bot.run(DISCORD_TOKEN)

if __name__ == "__main__":
    main()