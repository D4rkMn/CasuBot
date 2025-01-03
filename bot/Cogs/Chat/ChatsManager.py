from bot.Cogs.Chat.iLlmConnector import iLlmConnector, Message
from bot.Cogs.Chat.LlmResponseProcessor import LlmResponseProcessor
from typing import Dict, List

#
#   ChatsManager
#   Class that manages the chatting and response system
#   Acts like a bridge between the ChatCog and the LlmConnector        
#
class ChatsManager:
    def __init__(self, _llmConnector : iLlmConnector, _systemMessage : str):
        self.llmConnector = _llmConnector
        self.systemMessage : Message = Message(_username = "Sistema", _textContent = _systemMessage)
        self.chatDictionary : Dict[int, List[Message]] = {}

    def addLlmResponseToChannel(self, channel_id : int) -> List[Message]:
        chatlog = self.getChatlogFromChannel(channel_id)
        response = self.llmConnector.generateResponse(self.systemMessage, chatlog)
        response = LlmResponseProcessor.process(response)
        self.addMessageToChannel(channel_id, "Casu", response, None)
        return response

    def getChatlogFromChannel(self, channel_id : int) -> List[Message]:
        return self.chatDictionary[channel_id]

    def addMessageToChannel(self, channel_id : int, username : str, textContent : str, imageUrl : str):
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
        
        chatlog.append(Message(_username = username, _textContent = textContent, _imageUrl = imageUrl))