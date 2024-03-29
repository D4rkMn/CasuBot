from discord.ext import commands
from discord import Game

#
#   PresenceCog
#   Cog implementation to display the bots status and activity
#
class PresenceCog(commands.Cog):
    def __init__(self, _statusMessage : str):
        self.statusMessage = _statusMessage

    def assignBot(self, _bot):
        self.bot = _bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity = Game(name = self.statusMessage))

statusMessage = "c!help"
presenceCogInstance = PresenceCog(statusMessage)