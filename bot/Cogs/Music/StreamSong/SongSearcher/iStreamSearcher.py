from abc import ABC, abstractmethod
from typing import List
from bot.Cogs.Music.StreamSong.iStreamSong import iStreamSong

#
#   iStreamSearcher
#   Interface to hold different implementations of music searchers
#
class iStreamSearcher(ABC):
    @staticmethod
    @abstractmethod
    def search(searchQuery : str, resultLimit : int) -> List[iStreamSong]:
        pass