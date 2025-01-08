from discord.ext import commands

from dotenv import load_dotenv
import os
load_dotenv()

class UpdatesCog(commands.Cog):
    def __init__(self):
        DEBUG_MODE = os.getenv("DEBUG", "false").lower() == "true"
        if not DEBUG_MODE:
            self.botName = "CASU"
        else:
            self.botName = "DORITO"
    
    def assignBot(self, bot):
        self.bot = bot

    @commands.group()
    async def updates(self, ctx):
        pass

    @updates.command()
    async def changelog(self, ctx):
        text = self.__getTextFromFile("CHANGELOG")
        if text is None:
            return
        await ctx.send(text)

    @updates.command()
    async def todo(self, ctx):
        text = self.__getTextFromFile("TODO")
        if text is None:
            return
        await ctx.send(text)

    def __getTextFromFile(self, name : str) -> str | None:
        result = ""
        fileLocation = "bot/Cogs/Updates/" + name + ".txt"
        try:
            with open(fileLocation, "r") as f:
                for line in f.readlines():
                    result += line
            if result.strip() == "":
                return None
            result = f"**{self.botName} {name}:**\n" + result
            return result
        except FileNotFoundError:
            return None

updatesCogInstance = UpdatesCog()