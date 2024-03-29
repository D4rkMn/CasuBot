from bot.Cogs.Cubixo.iCubixoGenerator import iCubixoGenerator
from bot.Cogs.Cubixo.Cubixeador import Cubixeador

from discord.ext import commands

#
#   BirthdayCog
#   Cog implementation that contains bot commands related to Cubixo generation
#   Uses dependency injection to accept different Cubixo generators (why not lmao)
#
class CubixoCog(commands.Cog):
    def __init__(self, _cubixoGenerator : iCubixoGenerator):
        self.cubixoGenerator = _cubixoGenerator

    def assignBot(self, bot):
        self.bot = bot

    @commands.command()
    async def cubixo(self, ctx, arg : str = ""):
        reply = self.cubixoGenerator.generate(arg)
        await ctx.reply(reply)

cubixoGenerator = Cubixeador()
cubixoCogInstance = CubixoCog(cubixoGenerator)