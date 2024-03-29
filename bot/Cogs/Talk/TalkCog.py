from discord.ext import commands

#
#   TalkCog
#   A single command. Give it a text, and it will be repeated back at you
#
class TalkCog(commands.Cog):
    def assignBot(self, _bot):
        self.bot = _bot

    # seriously??? did we really need an entire cog for this shit?
    @commands.command()
    async def talk(self, ctx, *, arg):
        await ctx.reply(arg)

talkCogInstance = TalkCog()