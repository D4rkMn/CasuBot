from abc import ABC, abstractmethod

#
#   SongInfo
#   Holds information about a song
#
class SongInfo:
    def __init__(self, _name : str, _artist : str, _duration : str, _id : str):
        self.name = _name
        self.artist = _artist
        self.duration = _duration
        self.id = _id

#
#   iStreamConnector
#   Interface to hold different implementations of classes that connect with their respective apps api to produce song info
#
class iStreamConnector(ABC):
    @staticmethod
    @abstractmethod
    def getType() -> str:
        pass

    @staticmethod
    @abstractmethod
    def getSongInfoByUrl(url : str) -> SongInfo:
        pass

    @staticmethod
    @abstractmethod
    def getAudioSourceById(id : str):
        pass