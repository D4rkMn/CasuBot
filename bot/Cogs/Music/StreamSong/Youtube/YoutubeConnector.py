import yt_dlp
from youtube_search import YoutubeSearch

from googleapiclient.discovery import build

from bot.Cogs.Music.StreamSong.ConnectorInterfaces.iStreamConnector import iStreamConnector, SongInfo
from bot.Cogs.Music.StreamSong.ConnectorInterfaces.iSearchableConnector import iSearchableConnector
from bot.Cogs.Music.StreamSong.ConnectorInterfaces.iPlaylistConnector import iPlaylistConnector, PlaylistInfo

from bot.Cogs.Music.StreamSong.Youtube.WeirdTimeFormatter import WeirdTimeFormatter

from typing import List
import re

from dotenv import load_dotenv
import os
load_dotenv()

API_KEY = os.environ.get("YOUTUBE_API_KEY")
youtube = build("youtube", "v3", developerKey = API_KEY)

YT_URL = "https://www.youtube.com/watch?v="

YT_DLP_OPTS={
    "format" : "bestaudio",
    "force_generic_extractor" : True,
    "noplaylist" : True,
    "postprocessors" : [{
        "key" : "FFmpegExtractAudio",
        "preferredcodec" : "mp3",
        "preferredquality" : "192"
    }],
}

def extractPlaylistId(url : str) -> str:
    pattern = r"(?:https?://)?(?:www\.)?(?:youtube\.com/.*(?:\?|&)list=|youtu\.be/)([a-zA-Z0-9_-]+)"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        return None

def extractVideoId(url : str) -> str:
    pattern = r"(?:https?://)?(?:www\.)?(?:youtube\.com/.*[?\s&]v=|youtu\.be/)([a-zA-Z0-9_-]{11})"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        return None

#
#   YoutubeConnector
#   Implements iStreamConnector, iSearchableConnector, iPlaylistConnector
#   Connects to Youtube's api to get song info. Can be searched and can use playlists
#
class YoutubeConnector(iStreamConnector, iSearchableConnector, iPlaylistConnector):
    @staticmethod
    def getType() -> str:
        return "Youtube"

    @staticmethod
    def searchQuery(searchQuery : str, resultLimit : int) -> List[SongInfo]:
        queriedVideos = YoutubeSearch(searchQuery, max_results = resultLimit).to_dict()
        searchResults = []

        for video in queriedVideos:
            name = video['title']
            artist = video['channel']
            duration = video['duration'] if video['duration'] != "0" else 'LIVE'
            id = video['id']

            song = SongInfo(name, artist, duration, id)
            searchResults.append(song)

        return searchResults
    
    @staticmethod
    def getSongInfoByUrl(url : str) -> SongInfo:
        _id = extractVideoId(url)

        if url is None:
            raise ValueError("Youtube video ID counldn't be found on given URL")

        request = youtube.videos().list(
            part = "snippet, contentDetails",
            id = _id
        )
        response = request.execute()

        item = response["items"][0]

        _name = item["snippet"]["title"]
        _artist = item["snippet"]["channelTitle"]
        
        unformattedDuration = item['contentDetails']['duration']
        _duration = WeirdTimeFormatter.format(unformattedDuration)

        return SongInfo(_name, _artist, _duration, _id)    
        
    @staticmethod
    def getPlaylistInfoByUrl(url : str) -> PlaylistInfo:
        playlistId = extractPlaylistId(url)

        if playlistId is None:
            return

        request = youtube.playlists().list(
            part = "snippet,contentDetails",
            id = playlistId
        )
        response = request.execute()
    
        item = response["items"][0]

        _name = item["snippet"]["title"]
        _uploader = item["snippet"]["channelTitle"]
        _totalVideos = item["contentDetails"]["itemCount"]    

        return PlaylistInfo(_name, _uploader, _totalVideos)

    @staticmethod
    def getSongsByPlaylistUrl(url : str) -> List[SongInfo]:
        playlistId = extractPlaylistId(url)

        if playlistId is None:
            return
        
        maxResults = 50
        nextPageToken = None

        infoArray = []

        while True:

            request = youtube.playlistItems().list(
                part = "snippet, contentDetails",
                playlistId = playlistId,
                maxResults = maxResults,
                pageToken = nextPageToken
            )
            response = request.execute()            

            for item in response["items"]:
                try:
                    _id = item["snippet"]["resourceId"]["videoId"]
                    songInfo = YoutubeConnector.getSongInfoByUrl(f"{YT_URL}{_id}")
                    infoArray.append(songInfo)
                except IndexError:
                    print("song is unavailable (probably hidden or something else)")
                    continue

            nextPageToken = response.get("nextPageToken")

            if not nextPageToken:
                break

        print("info array size: ",len(infoArray))

        return infoArray

    @staticmethod
    def detectIfUrlIsPlaylist(url: str) -> bool:
        videoPattern = r"(?:https?://)?(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]+)"
        playlistPattern = r"(?:https?://)?(?:www\.)?(?:youtube\.com/playlist\?list=|youtu\.be/playlist/)([a-zA-Z0-9_-]+)"

        if re.match(playlistPattern, url):
            return True
        elif re.match(videoPattern, url):
            return False
        else:
            raise ValueError("Url does not match to a Youtube video")

    @staticmethod
    def getAudioSourceById(id : str):        
        youtubeSongUrl = f"{YT_URL}{id}"
        streamUrl = ""
        
        try:

            with yt_dlp.YoutubeDL(YT_DLP_OPTS) as ydl:
                info = ydl.extract_info(youtubeSongUrl, download = False)
                streamUrl = info["url"]
        
            return streamUrl
        
        except yt_dlp.DownloadError:

            raise ValueError("Song is unavailable")