from bot.Cogs.Chat.iLlmConnector import iLlmConnector
from bot.Cogs.Chat.GptConnector import GptConnector
from bot.Cogs.Chat.ChatsManager import ChatsManager
from bot.Utility.ImageUrlExtractor import ImageUrlExtractor

from discord.ext import commands

from dotenv import load_dotenv
import os
load_dotenv()

def getStringFromFile(filename : str) -> str:
    result = ""
    with open(filename) as f: 
        for line in f.readlines():
            result += line
    return result

def getSystemMessage(debug : bool) -> str:
    prefix = "bot/Cogs/Chat/SystemMessages/"
    if not debug:
        return getStringFromFile(prefix + "Casu.txt")
    else:
        return getStringFromFile(prefix + "Dorito.txt")

#
#   ChatCog
#   Cog implementation that contains bot commands and listeners related to chatting with the bot
#   Uses dependency injection to accept different large language models if needed
#
class ChatCog(commands.Cog):
    def __init__(self, _llmConnector : iLlmConnector, _systemMessage : str):
        self.chatsManager = ChatsManager(_llmConnector,_systemMessage)

    def assignBot(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message) -> None:
        if message.author == self.bot.user:
            return

        if message.content.startswith('c!'):
            return
        
        if message.reference and message.content.isdigit():
            msg = await message.channel.fetch_message(message.reference.message_id)
            if msg.content.startswith("**RESULTADOS DE LA BÚSQUEDA:**"):
                return
        
        if self.bot.user.mentioned_in(message):
            await self.__handleReplying(message)
        
    async def __handleReplying(self, message) -> None:
        async with message.channel.typing():
            username = message.author.name
            channel_id = message.channel.id

            msg = self.__messagePingsToUsernames(message, message.content)
            imageUrl = ImageUrlExtractor.extract(message)

            self.chatsManager.addMessageToChannel(channel_id, username, msg, imageUrl)
            response = self.chatsManager.addLlmResponseToChannel(channel_id)

        await message.reply(response)
        return
    
    def __messagePingsToUsernames(self, ctx, message):
        mentioned=ctx.mentions
        
        reply=message

        for user in mentioned:
            reply = reply.replace(f"<@{user.id}>", user.name)

        return reply

GPT_API_KEY = os.environ.get("GPT_API_KEY") 
GPT_MAX_TOKENS = 250

llmConnector = GptConnector(GPT_API_KEY, GPT_MAX_TOKENS)

# Get if debug mode
DEBUG_MODE = os.getenv("DEBUG", "false").lower() == "true"
systemMessage = getSystemMessage(DEBUG_MODE)

chatCogInstance = ChatCog(llmConnector, systemMessage)