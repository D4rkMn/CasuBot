from abc import ABC, abstractmethod
from typing import List

#
#   Message
#   Class to hold messages
#
class Message:
    def __init__(self, _username :str , _textContent : str = None, _imagesArray : List[str] = []):
        self.username : str = _username
        self.textArray : List[str] = []
        if _textContent is not None:
            self.textArray.append(_textContent)
        self.imagesArray : List[str] = _imagesArray

#
#   iLlmConnector
#   Interface to hold different implementations of Large Language Model connectors 
#
class iLlmConnector(ABC):
    @abstractmethod
    def generateResponse(self, systemMessage : Message, chatlog : List[Message]) -> str:
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