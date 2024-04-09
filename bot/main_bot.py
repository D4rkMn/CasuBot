from discord.ext import commands
import asyncio

from bot.Cogs.Birthday.BirthdayCog import birthdayCogInstance
from bot.Cogs.SpeechBubble.SpeechBubbleCog import speechBubbleCogInstance
from bot.Cogs.Cubixo.CubixoCog import cubixoCogInstance
from bot.Cogs.Momo.MomoCog import momoCogInstance
from bot.Cogs.Chat.ChatCog import chatCogInstance
from bot.Cogs.Shitpost.ShitpostCog import shitpostCogInstance
from bot.Cogs.Presence.PresenceCog import presenceCogInstance
from bot.Cogs.Music.MusicCog import musicCogInstance
from bot.Cogs.Talk.TalkCog import talkCogInstance
from bot.Cogs.Help.HelpCog import helpCogInstance
from bot.Cogs.Reminders.ReminderCog import reminderCogInstance

cogsArray = [
    birthdayCogInstance,
    speechBubbleCogInstance,
    cubixoCogInstance,
    momoCogInstance,
    chatCogInstance,
    shitpostCogInstance,
    presenceCogInstance,
    musicCogInstance,
    talkCogInstance,
    helpCogInstance,
    reminderCogInstance
]

class CasuBot(commands.Bot):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    async def async_setup(self):
        for Cog in cogsArray:
            Cog.assignBot(self)
            await self.add_cog(Cog)

    def setup(self):
        asyncio.run(self.async_setup())