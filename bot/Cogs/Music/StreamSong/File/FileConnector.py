from urllib.parse import urlparse
from ffmpeg._probe import probe

from bot.Cogs.Music.StreamSong.ConnectorInterfaces.iStreamConnector import iStreamConnector, SongInfo

from bot.Cogs.Music.SecondsToDurationFormatter import SecondsToDurationFormatter

#
#   FileConnector
#   Implements of iStreamConnector
#   Connector to get file methods
#
class FileConnector(iStreamConnector):
    @staticmethod
    def getType() -> str:
        return "File"

    @staticmethod
    def getSongInfoByUrl(url : str) -> SongInfo:
        parsed_url = urlparse(url)
        path = parsed_url.path
        filename = path.split('/')[-1]
        
        seconds = int(float(probe(url)['format']['duration']))

        _name = filename
        _artist = "Audio File"
        _duration = SecondsToDurationFormatter.format(seconds)
        _id = url

        return SongInfo(_name, _artist, _duration, _id)
    
    @staticmethod
    def getAudioSourceById(id : str):
        return id