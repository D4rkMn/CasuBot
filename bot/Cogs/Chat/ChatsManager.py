from bot.Cogs.Chat.iLlmConnector import iLlmConnector
from bot.Cogs.Chat.LlmResponseProcessor import LlmResponseProcessor
from typing import Dict, List

class Message:
    def __init__(self, _username :str , _messageContent : str):
        self.username = _username
        self.messageContent = _messageContent

#
#   ChatsManager
#   Class that manages the chatting and response system
#   Acts like a bridge between the ChatCog and the LlmConnector        
#
class ChatsManager:
    def __init__(self, _llmConnector : iLlmConnector, _systemMessage : str):
        self.llmConnector = _llmConnector
        self.systemMessage = _systemMessage
        self.chatDictionary : Dict[int, List[Message]] = {}

    def addLlmResponseToChannel(self, channel_id : int) -> str:
        chatlog = self.getChatlogFromChannel(channel_id)
        response = self.llmConnector.generateResponse(chatlog)
        response = LlmResponseProcessor.process(response)
        self.addMessageToChannel(channel_id, "Casu", response)
        return response

    def getChatlogFromChannel(self, channel_id : int) -> str:
        chatlog = f"Sistema: {self.systemMessage} \n"
        messageHistory = self.chatDictionary[channel_id]
        
        for message in messageHistory:
            chatlog += f"{message.username}: {message.messageContent}\n"
        
        chatlog += "Casu: "

        return chatlog

    def addMessageToChannel(self, channel_id : int, username : str, messageContent : str):
        if channel_id not in self.chatDictionary:
            self.chatDictionary[channel_id] = []

        chatlog = self.chatDictionary[channel_id]

        # imposed a limit to avoid error when prompt is too long
        CHATLOG_LIMIT = 50

        if len(chatlog) >= CHATLOG_LIMIT:
            chatlog.pop(0)
            
            # avoid removing too much content if needed
            if chatlog[0].username == "Casu":
                chatlog.pop(0)
        
        chatlog.append(Message(username,messageContent))