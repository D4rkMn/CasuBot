from abc import ABC, abstractmethod
from typing import List

from bot.Cogs.Music.StreamSong.ConnectorInterfaces.iStreamConnector import SongInfo

#
#   iSearchableConnector
#   Interface that represents connectors that also allow searching for songs of their type
#
class iSearchableConnector(ABC):
    @staticmethod
    @abstractmethod
    def searchQuery(searchQuery : str, resultLimit : int) -> List[SongInfo]:
        pass