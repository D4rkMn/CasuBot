from typing import List

from bot.Cogs.Music.StreamSong.iStreamSong import iStreamSong
from bot.Cogs.Music.StreamSong.SongSearcher.YoutubeSearcher import YoutubeSearcher
from bot.Cogs.Music.StreamSong.SongSearcher.SpotifySearcher import SpotifySearcher

RESULT_LIMIT = 10

#
#   SongSearchRouter
#   Redirects you to other providers' searchers
#
class SongSearchRouter:
    @staticmethod
    def search(searchQuery : str, searchProvider : str) -> List[iStreamSong]:
        if searchProvider == "Youtube":
            return YoutubeSearcher.search(searchQuery, RESULT_LIMIT)
        if searchProvider == "Spotify":
            return SpotifySearcher.search(searchQuery, RESULT_LIMIT)