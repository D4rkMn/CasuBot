from abc import ABC, abstractmethod
from typing import List

from bot.Cogs.Music.StreamSong.ConnectorInterfaces.iStreamConnector import SongInfo

#
#   PlaylistInfo
#   Holds information about a playlist
#
class PlaylistInfo:
    def __init__(self, _name, _uploader, _totalVideos):
        self.name = _name
        self.uploader = _uploader
        self.totalVideos = _totalVideos

#
#   iPlaylistConnector
#   Interface that represents connectors that also allow playlist management and playback
#
class iPlaylistConnector(ABC):
    @staticmethod
    @abstractmethod
    def getPlaylistInfoByUrl(url : str) -> PlaylistInfo:
        pass

    @staticmethod
    @abstractmethod
    def getSongsByPlaylistUrl(url : str) -> List[SongInfo]:
        pass

    @staticmethod
    @abstractmethod
    def detectIfUrlIsPlaylist(url : str) -> bool:
        pass