from bot.Cogs.Music.UrlTypeDetector import UrlTypeDetector

from bot.Cogs.Music.StreamSong.ConnectorInterfaces.iPlaylistConnector import iPlaylistConnector
from bot.Cogs.Music.StreamSong.Youtube.YoutubeConnector import YoutubeConnector

#
#   PlaylistConnectorRouter
#   Redirects you to getting an instance of static method accesing
#
class PlaylistConnectorRouter:
    def getConnector(url : str) -> iPlaylistConnector:
        streamProvider = UrlTypeDetector.detect(url)

        if streamProvider == "Youtube":
            return YoutubeConnector
        if streamProvider == "Spotify":
            #return SpotifyConnector
            pass

        return False