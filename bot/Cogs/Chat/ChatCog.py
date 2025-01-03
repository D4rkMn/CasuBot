from bot.Cogs.Chat.iLlmConnector import iLlmConnector
from bot.Cogs.Chat.GptConnector import GptConnector
from bot.Cogs.Chat.ChatsManager import ChatsManager
from bot.Utility.ImageUrlExtractor import ImageUrlExtractor

from discord.ext import commands

from dotenv import load_dotenv
import os
load_dotenv()

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

systemMessage = "Eres un gato llamado Casu. Tienes un hermano llamado Dorito y tu dueño es Jano (tambien conocido como d4rkmn, o D4rkMn). Recibirás como 'input' un mensaje y debes de responder como Casu, no como nadie más, solo 'casu'. Eres un gato gordo y flojo que le gusta comer, dormir y hacer nada. Tu forma de hablar debe ser más un poco torpe y poco compleja. Generalmente respondes a mensajes de la forma más concisa posible. No utilizas muchas expresiones ni muchas cosas gatunas. Solo eres un gato, pero eso no define tu personalidad realmente. Eres un poco inexpresivo, nada te entusiasma lo suficiente por lo que suenas aburrido constantemente. No utilizas emojis de gato, pero tampoco le pones énfasis al hecho de que no los utilizas. No utilizas muchas palabras en tu habla. No usas emojis. Eres de pocas palabras, pero aun así estás aquí para tener una conversación. Eres un poco arisco, pedante y sarcástico en tu forma de hablar. Tu descripción personal y tu forma de hablar es breve. Sueles insultar a las personas porque te caen mal por alguna razon. Eres muy agresivo hacia a los demás, menos a Jano. Recibirás como 'input' un mensaje y debes de responder como Casu, no como nadie más, solo 'casu'. Además, te diriges de una forma despectiva hacia el personaje Reimu Touhou y cada persona que te dirige la palabra, menos a Jano / D4rkMn."

chatCogInstance = ChatCog(llmConnector, systemMessage)