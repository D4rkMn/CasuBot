from abc import ABC, abstractmethod
from discord import FFmpegPCMAudio

#
#   iStreamSong
#   Interface to hold different implementations of songs by different streaming providers
#
class iStreamSong(ABC):
    @abstractmethod
    def createFromUrl(self, url : str) -> None:
        pass

    @abstractmethod
    def createFromDetails(self, _name : str, _artist : str, _duration : str, _id : str) -> None:
        pass

    @abstractmethod
    def getAudioStream(self) -> FFmpegPCMAudio:
        pass