from abc import ABC, abstractmethod
from typing import List

#
#   Message
#   Class to hold messages
#
class Message:
    def __init__(self, _username :str , _textContent : str = None, _imageUrl : str = None):
        self.username : str = _username
        self.textContent : str = _textContent
        self.imageUrl : str = _imageUrl

#
#   iLlmConnector
#   Interface to hold different implementations of Large Language Model connectors 
#
class iLlmConnector(ABC):
    @abstractmethod
    def generateResponse(self, inputText : str) -> str:
        pass

    def generateMessageList(self, systemMessage : Message, chatlog : List[Message]):
        result = []
        result.append(self.processMessage(systemMessage))
        for message in chatlog:
            result.append(self.processMessage(message))
        return result

    @abstractmethod
    def processMessage(self, message : Message):
        pass