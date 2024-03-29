from abc import ABC, abstractmethod

#
#   iCubixoGenerator
#   Interface to hold different implementations of Cubixo generators 
#
class iCubixoGenerator(ABC):
    @abstractmethod
    def generate(self, text : str) -> str:
        pass