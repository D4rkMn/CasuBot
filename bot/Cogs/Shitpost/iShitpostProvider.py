from abc import ABC, abstractmethod

#
#   iShitpostProvider
#   Interface to hold different implementations of shitpost providers
#
class iShitpostProvider(ABC):
    @abstractmethod
    def getShitpost(self) -> str:
        pass