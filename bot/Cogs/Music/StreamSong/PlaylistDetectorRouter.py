from bot.Cogs.Music.UrlTypeDetector import UrlTypeDetector

from bot.Cogs.Music.StreamSong.Youtube.YoutubeConnector import YoutubeConnector

#
#   PlaylistDetectorRouter
#   Redirects you to other providers' playlist detection
#
class PlaylistDetectorRouter:
    def detect(url : str) -> bool:
        streamProvider = UrlTypeDetector.detect(url)

        if streamProvider == "Youtube":
            return YoutubeConnector.detectIfUrlIsPlaylist(url)
        if streamProvider == "Spotify":
            #return SpotifyConnector.detectIfUrlIsPlaylist(url)
            pass

        return False