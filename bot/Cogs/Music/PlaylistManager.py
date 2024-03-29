from bot.Cogs.Music.StreamSong.iStreamSong import iStreamSong
from bot.Cogs.Music.StreamSong.StreamSongFactory import StreamSongFactory
from bot.Cogs.Music.StreamSong.SongSearcher.SongSearchRouter import SongSearchRouter
from bot.Cogs.Music.StreamSong.PlaylistConnectorRouter import PlaylistConnectorRouter, iPlaylistConnector
from bot.Cogs.Music.StreamSong.PlaylistDetectorRouter import PlaylistDetectorRouter
from bot.Cogs.Music.StreamSong.ConnectorInterfaces.iPlaylistConnector import PlaylistInfo
from typing import List
import random

#
#   PlaylistManager
#   Manages a music playlist for a single voice channel
#
class PlaylistManager:
    def __init__(self):
        self.songList : List[iStreamSong] = [] # the playlist itself
        self.currentSongIndex = 0 # index of the song currently playing in the song list
        self.currentTimestamp = 0 # time played in seconds

        self.isPlayingStopped = False # if playing was stopped
        self.goingNext = False # if in process of changing to the next song in queue
        self.goingPrev = False # if in process of changing to the previous song in queue
        
        self.isSongLooping = False # if a song is currently looping
        self.isPlaylistLooping = False # if the entire playlist is looping

    def getSongsBySearch(self, searchQuery : str, searchProvider : str) -> List[iStreamSong]:
        searchResults = SongSearchRouter.search(searchQuery, searchProvider)
        return searchResults

    def detectIfPlaylist(self, url : str) -> bool:
        return PlaylistDetectorRouter.detect(url)
    
    def getConnectorByUrl(self, url : str) -> iPlaylistConnector:
        return PlaylistConnectorRouter.getConnector(url)

    def getPlaylistInfoByUrl(self, url : str, playlistConnector : iPlaylistConnector) -> PlaylistInfo:
        return playlistConnector.getPlaylistInfoByUrl(url)

    def getSongsByPlaylistUrl(self, url : str, playlistConnector : iPlaylistConnector) -> List[iStreamSong]:
        songInfoArray = playlistConnector.getSongsByPlaylistUrl(url)
        songArray = []
        
        for songInfo in songInfoArray:
            song : iStreamSong = StreamSongFactory.createEmptySongFromConnector(playlistConnector)
            song.createFromDetails(songInfo.name, songInfo.artist, songInfo.duration, songInfo.id)
            songArray.append(song)

        return songArray

    def getSongByUrl(self, url : str) -> iStreamSong:
        song = StreamSongFactory.createSongFromUrl(url)
        return song

    def addSongToPlaylist(self, song : iStreamSong) -> None:
        self.songList.append(song)

    def clearPlaylist(self) -> None:
        self.songList = []
        self.currentSongIndex = 0

    def loopCurrentSong(self) -> bool:
        self.isSongLooping = not self.isSongLooping
        return self.isSongLooping

    def loopPlaylist(self) -> bool:
        self.isPlaylistLooping = not self.isPlaylistLooping
        return self.isPlaylistLooping
    
    def stopCurrentSong(self) -> None:
        self.resetTimestamp()
        self.isPlayingStopped = True

    def resumeCurrentSong(self) -> None:
        self.isPlayingStopped = False

    def playCurrentSong(self):
        currentSong : iStreamSong = self.songList[self.currentSongIndex]
        audioStream = currentSong.getAudioStream()
        return audioStream
    
    def handleNextSong(self) -> None:
        if self.isSongLooping and not (self.goingNext or self.goingPrev):
            return
        
        if self.isPlayingStopped:
            return
        
        step = 1
        
        if self.goingNext:
            self.stopGoingNextSong()
        elif self.goingPrev:
            self.stopGoingPrevSong()
            step = -1
        
        if self.isPlaylistLooping:
            self.currentSongIndex += step
            self.currentSongIndex %= len(self.songList)
            return
        
        self.currentSongIndex += step
        self.currentSongIndex %= len(self.songList) + 1

    def startGoingNextSong(self) -> None:
        self.goingNext = True

    def stopGoingNextSong(self) -> None:
        self.goingNext = False

    def startGoingPrevSong(self) -> None:
        self.goingPrev = True

    def stopGoingPrevSong(self) -> None:
        self.goingPrev = False

    def addCountToTimestamp(self) -> None:
        self.currentTimestamp += 1

    def resetTimestamp(self) -> None:
        self.currentTimestamp = 0

    def getCurrentTimestamp(self) -> int:
        return self.currentTimestamp

    def getCurrentPlaylist(self) -> str:
        if len(self.songList) == 0:
            return "La cola de canciones está vacía!"

        if len(self.songList) > 20:
            return self.__formatQueueOverfilled()

        return self.__formatQueueEnough()
    
    def __formatQueueOverfilled(self) -> str:
        reply = "**COLA DE CANCIONES:**\n"

        middleAmount = 9
        lowIndex = self.currentSongIndex - middleAmount
        highIndex = self.currentSongIndex + middleAmount

        if lowIndex < 0:
            highIndex -= lowIndex
            lowIndex = 0
        elif highIndex >= len(self.songList):
            lowIndex -= highIndex - len(self.songList)
            highIndex = len(self.songList) - 1

        if lowIndex != 0:
            reply += "...\n"

        for i in range(lowIndex, highIndex + 1):
            song = self.songList[i]

            # higlight the current song
            if i == self.currentSongIndex:
                reply += f"**{i+1}: {song.name} - {song.artist} - {song.duration}**\n"
            
            else:                
                reply += f"{i+1}: {song.name} - {song.artist} - {song.duration}\n"

        if highIndex != len(self.songList) - 1:
            reply += "...\n"

        return reply
    
    def __formatQueueEnough(self) -> str:
        reply = "**COLA DE CANCIONES:**\n"

        for i in range(len(self.songList)):
            song = self.songList[i]

            # higlight the current song
            if i == self.currentSongIndex:
                reply += f"**{i+1}: {song.name} - {song.artist} - {song.duration}**\n"
            
            else:                
                reply += f"{i+1}: {song.name} - {song.artist} - {song.duration}\n"

        return reply
    
    def getCurrentSong(self) -> iStreamSong:
        return self.songList[self.currentSongIndex]
    
    def shufflePlaylist(self) -> None:
        song = self.getCurrentSong()
        tempList = [item for item in self.songList if item != song]
        random.shuffle(tempList)
        self.songList = [song] + tempList
        self.currentSongIndex = 0

    def skipToIndex(self, index : str, clientPlaying : bool) -> None:
        if not self.isIndexInBounds(index):
            raise TypeError("Invalid index")
        
        index = int(index)
        self.currentSongIndex = index - 1 - int(clientPlaying)

    def removeIndex(self, index : str) -> None:
        if not self.isIndexInBounds(index):
            raise TypeError("Invalid index")
        
        index = int(index) - 1

        if index == self.currentSongIndex:
            raise ValueError("Cant remove index of currently playing song")
        
        self.songList.pop(index)
        
    def isIndexInBounds(self, index : str) -> bool:
        try:
            index = int(index) 
            if index < 1 or index > len(self.songList):
                return False
            return True
        except:
            return False