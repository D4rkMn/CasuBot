from discord.ext import commands
from bot.Cogs.Music.MusicHelp import MusicHelp
from bot.Cogs.Chat.ChatHelp import ChatHelp
from bot.Cogs.SpeechBubble.GloboHelp import GloboHelp
from bot.Cogs.Momo.MomoHelp import MomoHelp
from bot.Cogs.Birthday.BirthdayHelp import BirthdayHelp
from bot.Cogs.Shitpost.ShitpostHelp import ShitpostHelp
from bot.Cogs.Cubixo.CubixoHelp import CubixoHelp
from bot.Cogs.Talk.TalkHelp import TalkHelp

#
#   HelpCog
#   Cog implementation that holds help commands for other cogs
#
class HelpCog(commands.Cog):
    def assignBot(self, _bot):
        self.bot = _bot

    @commands.group(invoke_without_command = True)
    async def help(self, ctx):
        reply = """**AYUDA COMANDOS:**
- c!help: Muestra los comandos de ayuda (estás aquí)
- c!help music: Muestra los comandos de música
- c!help chat: Muestra los comandos de chat
- c!help globo: Muestra los comandos de globo
- c!help momo: Muestro los comandos de momo
- c!help cum: Muestra los comandos de cumpleaños
- c!help shitpost: Muestra los comandos de shitpost
- c!help cubixo: Muestra los comandos de cubixo
- c!help talk: Muestra los comandos de hablar
"""
        await ctx.reply(reply)

    @help.command()
    async def music(self, ctx):
        reply = MusicHelp.message()
        await ctx.reply(reply)

    @help.command()
    async def chat(self, ctx):
        reply = ChatHelp.message()
        await ctx.reply(reply)
    
    @help.command()
    async def globo(self, ctx):
        reply = GloboHelp.message()
        await ctx.reply(reply)
        
    @help.command()
    async def momo(self, ctx):
        reply = MomoHelp.message()
        await ctx.reply(reply)
        
    @help.command()
    async def cum(self, ctx):
        reply = BirthdayHelp.message()
        await ctx.reply(reply)
        
    @help.command()
    async def shitpost(self, ctx):
        reply = ShitpostHelp.message()
        await ctx.reply(reply)
        
    @help.command()
    async def cubixo(self, ctx):
        reply = CubixoHelp.message()
        await ctx.reply(reply)

    @help.command()
    async def talk(self, ctx):
        reply = TalkHelp.message()
        await ctx.reply(reply)

helpCogInstance = HelpCog()