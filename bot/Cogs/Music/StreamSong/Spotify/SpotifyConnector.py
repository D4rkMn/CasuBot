import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from librespot.core import Session
from librespot.metadata import TrackId
from librespot.audio.decoders import AudioQuality, VorbisOnlyAudioQuality

from bot.Cogs.Music.StreamSong.ConnectorInterfaces.iStreamConnector import iStreamConnector, SongInfo
from bot.Cogs.Music.StreamSong.ConnectorInterfaces.iSearchableConnector import iSearchableConnector
from bot.Cogs.Music.StreamSong.ConnectorInterfaces.iPlaylistConnector import iPlaylistConnector, PlaylistInfo

from bot.Cogs.Music.SecondsToDurationFormatter import SecondsToDurationFormatter

from typing import List
import re

from dotenv import load_dotenv
import os
load_dotenv()

CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")

SPOTIFY_USER = os.environ.get("SPOTIFY_USER")
SPOTIFY_PASS = os.environ.get("SPOTIFY_PASS")

clientCredentialsManager = SpotifyClientCredentials(client_id = CLIENT_ID, client_secret = CLIENT_SECRET)
spotify : spotipy.Spotify = spotipy.Spotify(client_credentials_manager = clientCredentialsManager)

while True:
    try:
        librespotSession = Session.Builder() \
            .user_pass(SPOTIFY_USER, SPOTIFY_PASS) \
            .create()
        break
    except:
        print("error logging in to librespot")
        pass

def extractPlaylistId(url : str) -> str:
    pattern = r'/playlist/([a-zA-Z0-9]+)'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        return None

#
#   SpotifyConnector
#   Implements iStreamConnector, iSearchableConnector, iPlaylistConnector
#   Connects to Spotify's api to get song info. Can be searched and can use playlists
#
class SpotifyConnector(iStreamConnector, iSearchableConnector, iPlaylistConnector):
    @staticmethod
    def getType() -> str:
        return "Spotify"

    @staticmethod
    def searchQuery(searchQuery : str, resultLimit : int) -> List[SongInfo]:
        queriedSongs = spotify.search(q = searchQuery, type ="track", limit = resultLimit)
        searchResults = []

        for track in queriedSongs['tracks']['items']:
            name = track["name"]
            artist = track["artists"][0]["name"]
            seconds = track["duration_ms"] // 1000
            duration = SecondsToDurationFormatter.format(seconds)
            id = track["id"]

            song = SongInfo(name, artist, duration, id)
            searchResults.append(song)

        return searchResults
    
    @staticmethod
    def getSongInfoByUrl(url : str) -> SongInfo:
        track = spotify.track(url)

        _name = track["name"]
        _artist = track["artists"][0]["name"]
        seconds = track["duration_ms"] // 1000
        _duration = SecondsToDurationFormatter.format(seconds)
        _id = track["id"]

        return SongInfo(_name, _artist, _duration, _id)

    @staticmethod
    def getPlaylistInfoByUrl(url: str) -> PlaylistInfo:
        playlistId = extractPlaylistId(url)

        if playlistId is None:
            return
        
        response = spotify.playlist(playlistId)

        _name = response['name']
        _uploader = response['owner']['display_name']
        _totalVideos = len(response['tracks']['items'])

        return PlaylistInfo(_name, _uploader, _totalVideos)

    @staticmethod
    def getSongsByPlaylistUrl(url: str) -> List[SongInfo]:
        playlistId = extractPlaylistId(url)

        if playlistId is None:
            return
        
        response = spotify.playlist_tracks(playlistId)

        infoArray = []

        for track in response['items']:
            item = track['track']

            _name = item['name']
            _artist = item['artists'][0]['name']
            _id = item['id']
            
            milliseconds = item['duration_ms']
            _duration = SecondsToDurationFormatter.format(milliseconds // 1000)

            songInfo = SongInfo(_name, _artist, _duration, _id)
            infoArray.append(songInfo)

        return infoArray

    @staticmethod
    def detectIfUrlIsPlaylist(url: str) -> bool:
        playlistPattern = r"(?:https?://)?(?:www\.)?(?:open\.spotify\.com/playlist/|spotify\.com/playlist/)([a-zA-Z0-9]+)"
        if re.match(playlistPattern, url):
            return True
        else:
            return False

    @staticmethod
    def getAudioSourceById(id : str):
        songUri = TrackId.from_uri(f"spotify:track:{id}")

        while True:
            try:
                result = librespotSession.content_feeder().load(songUri, VorbisOnlyAudioQuality(AudioQuality.NORMAL), False, None)
                audioStream = result.input_stream.stream()
                return audioStream
            except ValueError:
                pass
            except OSError:
                pass