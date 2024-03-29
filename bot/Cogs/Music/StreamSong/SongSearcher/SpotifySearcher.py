from bot.Cogs.Music.StreamSong.SongSearcher.iStreamSearcher import iStreamSearcher
from bot.Cogs.Music.StreamSong.iStreamSong import iStreamSong
from bot.Cogs.Music.StreamSong.Spotify.SpotifySong import SpotifySong
from bot.Cogs.Music.StreamSong.Spotify.SpotifyConnector import SpotifyConnector
from bot.Cogs.Music.SecondsToDurationFormatter import SecondsToDurationFormatter
from typing import List

#
#   SpotifySearcher
#   Implementation of iStreamSearcher
#   Searches for songs in spotify and returns a list of spotify songs
#
class SpotifySearcher(iStreamSearcher):
    @staticmethod
    def search(searchQuery: str, resultLimit : int) -> List[SpotifySong]:
        queriedSongs = SpotifyConnector.searchQuery(searchQuery, resultLimit)
        searchResults = []

        for song in queriedSongs:
            spotifySong = SpotifySong()
            spotifySong.createFromDetails(song.name, song.artist, song.duration, song.id)
            searchResults.append(spotifySong)

        return searchResults