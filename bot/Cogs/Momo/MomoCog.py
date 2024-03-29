from discord.ext import commands
from discord import File
from bot.Cogs.Momo.MomoGenerator import MomoGenerator
from bot.Utility.QuotationMarkSplitter import QuotationMarkSplitter

class UrlTextPair:
    def __init__(self, _url : str, _text : str):
        self.url = _url
        self.text = _text

#
#   MomoCog
#   Cog implementation that contains bot commands to generate momos
#
class MomoCog(commands.Cog):
    def assignBot(self, bot):
        self.bot = bot

    @commands.command()
    async def momo(self, ctx, *, arg = ""):
        if arg == "":
            await ctx.reply("No haz añadido ningun texto tonto weon")
            return

        if not ctx.message.attachments:
            await ctx.reply('No haz añadido ninguna imagen tonto weon')
            return

        textList = QuotationMarkSplitter.split(arg)
        pairList = [] # UrlTextPair list

        for i in range(len(ctx.message.attachments)):
            if i >= len(textList):
                break

            url = ctx.message.attachments[i].url
            text = textList[i]

            pairList.append(UrlTextPair(url, text))

        imagePath = MomoGenerator.generate(*pairList)

        if imagePath is None: # if image couldnt be generated for some reason
            await ctx.reply("No haz añadido ningun texto tonto weon")
            return

        with open(imagePath,'rb') as file:
            result = File(file)
            await ctx.reply(file = result)
        
        MomoGenerator.removeImageFromPath(imagePath)

momoCogInstance = MomoCog()