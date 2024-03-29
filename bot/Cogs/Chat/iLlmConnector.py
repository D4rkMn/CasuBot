from abc import ABC, abstractmethod

#
#   iLlmConnector
#   Interface to hold different implementations of Large Language Model connectors 
#
class iLlmConnector(ABC):
    @abstractmethod
    def generateResponse(inputText : str) -> str:
        pass