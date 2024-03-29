from discord.ext import commands
from discord import File
from bot.Cogs.SpeechBubble.SpeechBubbleGenerator import SpeechBubbleGenerator
from bot.Utility.ImageUrlExtractor import ImageUrlExtractor
from aiostream import stream

#
#   SpeechBubbleCog
#   Cog implementation that contains bot commands to generate speech bubble images
#
class SpeechBubbleCog(commands.Cog):
    def assignBot(self, bot):
        self.bot = bot

    @commands.command()
    async def globo(self, ctx):
        url = ImageUrlExtractor.extract(ctx.message)
        
        # if no image attached
        if url is None:
            # if reply exists
            if ctx.message.reference is not None:
                await self.addBubbleToReply(ctx)
            else:
                await self.addBubbleToLastImage(ctx)
        
        # if image attached
        else:
            # if reply exists
            if ctx.message.reference is not None:
                await self.replyWithBubble(ctx,url)
            else:
                await self.sendSpeechBubble(ctx, url)

    async def replyWithBubble(self, ctx, url):
        reply = ctx.message.reference
        
        if reply is None:
            # how did we get here???
            return None # why?
        
        reply_ctx = await ctx.channel.fetch_message(reply.message_id)

        await self.sendSpeechBubble(reply_ctx, url)

    async def addBubbleToReply(self, ctx):
        reply=ctx.message.reference
        
        if reply is None:
            # how did we get here???
            return None # why?
        
        msg = await ctx.channel.fetch_message(reply.message_id)

        url = ImageUrlExtractor.extract(msg)

        if url is None:
            await ctx.reply('Eso no es una imagen ah')
            return None
        
        await self.sendSpeechBubble(ctx, url)

    async def addBubbleToLastImage(self, ctx):
        HISTORY_LIMIT = 100 # how many messages we are going to be searching for
        messages = await stream.list(ctx.channel.history(limit = HISTORY_LIMIT))

        selected=None

        for message in messages:
            if message.author.id == self.bot.user.id:
                continue

            if len(message.attachments) > 0 or len(message.embeds) > 0:
                selected = message
                break

        if selected is None:
            await ctx.reply(f"No se ha encontrado una imagen entre los ultimos {HISTORY_LIMIT} mensajes")
            return
        
        url = ImageUrlExtractor.extract(selected)
        await self.sendSpeechBubble(ctx, url)

    async def sendSpeechBubble(self, ctx, url):
        resultPath = SpeechBubbleGenerator.generateFromUrl(url)
        
        with open(resultPath, 'rb') as resultFile:
            result = File(resultFile)
            await ctx.reply(file = result)
            
        SpeechBubbleGenerator.removeImageFromPath(resultPath)

speechBubbleCogInstance = SpeechBubbleCog()