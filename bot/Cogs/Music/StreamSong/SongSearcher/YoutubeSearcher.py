from bot.Cogs.Music.StreamSong.SongSearcher.iStreamSearcher import iStreamSearcher
from bot.Cogs.Music.StreamSong.iStreamSong import iStreamSong
from bot.Cogs.Music.StreamSong.Youtube.YoutubeSong import YoutubeSong
from bot.Cogs.Music.StreamSong.Youtube.YoutubeConnector import YoutubeConnector
from typing import List

#
#   YoutubeSearcher
#   Implementation of iStreamSearcher
#   Searches for songs in youtube and returns a list of youtube songs
#
class YoutubeSearcher(iStreamSearcher):
    @staticmethod
    def search(searchQuery: str, resultLimit : int) -> List[YoutubeSong]:
        queriedSongs = YoutubeConnector.searchQuery(searchQuery, resultLimit)
        searchResults = []

        for song in queriedSongs:
            youtubeSong = YoutubeSong()
            youtubeSong.createFromDetails(song.name, song.artist, song.duration, song.id)
            searchResults.append(youtubeSong)

        return searchResults