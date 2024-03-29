import random
from discord.ext import commands
from bot.Cogs.Shitpost.iShitpostProvider import iShitpostProvider
from bot.Cogs.Shitpost.TheDailyShitpostProvider import TheDailyShitpostProvider

#
#   ShitpostCog
#   Cog implementation that contains bot commands to send shitposts
#
class ShitpostCog(commands.Cog):
    def __init__(self, _shitpostProvider : iShitpostProvider):
        self.shitpostProvider = _shitpostProvider

    def assignBot(self, bot) -> None:
        self.bot = bot

    @commands.command()
    async def shitpost(self, ctx) -> None:
        result = self.shitpostProvider.getShitpost()
        if result:
            await ctx.reply(result)

    @commands.Cog.listener()
    async def on_message(self, message) -> None:
        if message.author == self.bot.user:
            return

        if message.content.startswith('c!'):
            return
        
        if random.randint(1, shitpostRNG) == 1:
            await self.shitpost(message)

# chance to randomly get a shitpost from sending a message
shitpostRNG = 1000

shitpostProvider = TheDailyShitpostProvider()
shitpostCogInstance = ShitpostCog(shitpostProvider)