from bot.Cogs.Music.StreamSong.iStreamSong import iStreamSong
from bot.Cogs.Music.StreamSong.Spotify.SpotifyConnector import SpotifyConnector
from bot.Cogs.Music.FfmpegAudioFactory import FfmpegAudioFactory
from discord import FFmpegPCMAudio

#
#   SpotifySong
#   Implementation of iStreamSong
#   Holds information about a song streamed via spotify
#
class SpotifySong(iStreamSong):
    def createFromUrl(self, url : str) -> None:
        songInfo = SpotifyConnector.getSongInfoByUrl(url)
        self.createFromDetails(songInfo.name, songInfo.artist, songInfo.duration, songInfo.id)

    def createFromDetails(self, _name : str, _artist : str, _duration : str, _id : str) -> None:
        self.name = _name
        self.artist = _artist
        self.duration = _duration
        self.id = _id

    def getAudioStream(self) -> FFmpegPCMAudio:
        audioSource = SpotifyConnector.getAudioSourceById(self.id)
        ffmpeg = FfmpegAudioFactory.create(source = audioSource, pipe = True)
        return ffmpeg