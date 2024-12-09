from bot.Cogs.Music.SecondsToDurationFormatter import SecondsToDurationFormatter
from bot.Cogs.Music.UrlTypeDetector import UrlTypeDetector
from bot.Cogs.Music.StreamSong.ConnectorInterfaces.iStreamConnector import iStreamConnector

from bot.Cogs.Music.StreamSong.iStreamSong import iStreamSong
from bot.Cogs.Music.StreamSong.Youtube.YoutubeSong import YoutubeSong
from bot.Cogs.Music.StreamSong.File.FileSong import FileSong

#
#   StreamSongFactory
#   Factory to create different types of songs given different parameters
#
class StreamSongFactory:
    @staticmethod
    def createSongFromUrl(url : str) -> iStreamSong:
        streamProvider = UrlTypeDetector.detect(url)
        song : iStreamSong = None

        if streamProvider == "Youtube":
            song = YoutubeSong()
        elif streamProvider == "Spotify":
            raise ValueError("Spotify has been deprecated")
        elif streamProvider == "File":
            song = FileSong()

        song.createFromUrl(url)
        return song
    
    @staticmethod
    def createEmptySongFromConnector(connector : iStreamConnector) -> iStreamSong:
        if connector.getType() == "Youtube":
            return YoutubeSong()
        if connector.getType() == "Spotify":
            raise ValueError("Spotify has been deprecated")
        if connector.getType() == "File":
            return FileSong()

    @staticmethod
    def createSongFromDetails(songName : str, songArtist : str, songTimeSeconds : int, songId : str, streamProvider : str) -> iStreamSong:
        songDuration = SecondsToDurationFormatter.format(songTimeSeconds)

        if streamProvider == "Youtube":
            song = YoutubeSong()
        elif streamProvider == "Spotify":
            raise ValueError("Spotify has been deprecated")

        song.createFromDetails(songName, songArtist, songDuration, songId)
        return song