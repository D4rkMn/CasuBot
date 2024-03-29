from abc import ABC, abstractmethod

#
#   iCommandHelp
#   Interface to hold different help messages for different commands 
#
class iCommandHelp(ABC):
    @staticmethod
    @abstractmethod
    def message() -> str:
        pass