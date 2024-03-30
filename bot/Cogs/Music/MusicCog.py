from discord.ext import commands
from discord import ClientException
from bot.Cogs.Music.PlaylistManager import PlaylistManager
from bot.Utility.UrlValidator import UrlValidator
from bot.Cogs.Music.SecondsToDurationFormatter import SecondsToDurationFormatter
from bot.Cogs.Music.StreamSong.iStreamSong import iStreamSong
from typing import Dict
import asyncio

WAITING_TIMEOUT = 60

#
#   MusicCog
#   Cog implementation that contains bot commands and listeners related to playing music
#
class MusicCog(commands.Cog):
    def __init__(self):
        self.playlistDict : Dict[int, PlaylistManager] = {} # (key: channelId, value : PlaylistManager for said voice channel)

    def assignBot(self, bot):
        self.bot : commands.Bot = bot

    @commands.Cog.listener()
    async def on_message(self, message) -> None:
        if message.author == self.bot.user:
            return

        if message.content.startswith('c!'):
            return

        if message.reference and message.content.isdigit():
            msg = await message.channel.fetch_message(message.reference.message_id)
            if msg.content.startswith("**RESULTADOS DE LA BÚSQUEDA:**"):
                return

    @commands.group()
    async def music(self, ctx):
        pass

    @music.command()
    async def join(self, ctx) -> bool:
        if not ctx.message.author.voice:
            await ctx.send("No estas conectado a un canal de voz tonto weon")
            return False
        
        voiceChannel = ctx.message.author.voice.channel

        try:
            await voiceChannel.connect()
        except ClientException: # if already connected
            pass
        finally:
            channelId = ctx.author.voice.channel.id
            if channelId not in self.playlistDict:
                self.playlistDict[channelId] = PlaylistManager()
            return True
        
    @music.command()
    async def leave(self, ctx):
        voiceClient=ctx.message.guild.voice_client

        if voiceClient is None:
            await ctx.send('No estoy conectado a un canal de voz tonto weon')
            return

        if not voiceClient.is_connected():
            await ctx.send('No estas conectado a un canal de voz tonto weon')
            return

        await voiceClient.disconnect()

        channelId = ctx.author.voice.channel.id
        self.playlistDict.pop(channelId)

    @music.command()
    async def play(self, ctx, *, arg = None):
        if ctx.message.attachments:
            await self.addFile(ctx)
        else:
            await self.addArg(ctx, arg)

    @music.group(invoke_without_command = True)
    async def search(self, ctx, *, arg = None):
        await self.searchAndPlay(ctx, arg, "Youtube")

    @search.command()
    async def yt(self, ctx, *, searchQuery):
        await self.searchAndPlay(ctx, searchQuery, "Youtube")

    @search.command()
    async def sp(self, ctx, *, searchQuery):
        await self.searchAndPlay(ctx, searchQuery, "Spotify")

    async def searchAndPlay(self, ctx, searchQuery : str, searchProvider : str) -> None:
        isJoined = await self.join(ctx)
        
        if not isJoined:
            return
        
        channel = ctx.author.voice.channel
        channelId = channel.id
        voiceClient = ctx.message.guild.voice_client

        if not voiceClient.is_connected():
            print("bot voice client isnt connected despite having joined (?")
            return
        
        if searchQuery == "":
            await ctx.reply("Tienes que escribir algo para buscar!")
            return
        
        song = await self.searchByQuery(ctx, searchQuery, searchProvider)
        if song is None:
            return
        
        self.playlistDict[channelId].addSongToPlaylist(song)
        await ctx.reply(f"Se añadió **{song.name}** - **{song.artist}** a la cola!")

        self.playlistDict[channelId].resumeCurrentSong()

        if not voiceClient.is_playing():
            await self.playSong(ctx, channelId)

    async def addFile(self, ctx):
        attachment = ctx.message.attachments[0]
        await self.addArg(ctx, attachment.url)

    async def addArg(self, ctx, arg):
        isJoined = await self.join(ctx)
        
        if not isJoined:
            return
        
        channel = ctx.author.voice.channel
        channelId = channel.id
        voiceClient = ctx.message.guild.voice_client

        if not voiceClient.is_connected():
            print("bot voice client isnt connected despite having joined (?")
            return
        
        if arg != "":
            isArgUrl = UrlValidator.check(arg)

            song : iStreamSong = None

            if isArgUrl:

                isPlaylist = self.playlistDict[channelId].detectIfPlaylist(arg)

                if isPlaylist:
                    await self.addPlaylist(ctx, arg)
                    return

                song = self.playlistDict[channelId].getSongByUrl(arg)
            
            else:
                song = await self.searchByQuery(ctx, arg)
                if song is None:
                    return
            
            self.playlistDict[channelId].addSongToPlaylist(song)
            await ctx.reply(f"Se añadió **{song.name}** - **{song.artist}** a la cola!")

        self.playlistDict[channelId].resumeCurrentSong()

        if not voiceClient.is_playing():
            await self.playSong(ctx, channelId)

    async def addPlaylist(self, ctx, url : str) -> None:
        channelId = ctx.author.voice.channel.id
        voiceClient = ctx.message.guild.voice_client
        connector = self.playlistDict[channelId].getConnectorByUrl(url)
        playlistInfo = self.playlistDict[channelId].getPlaylistInfoByUrl(url, connector)
        songsArray = self.playlistDict[channelId].getSongsByPlaylistUrl(url, connector)
        
        await ctx.reply(f"Se añadió la playlist **{playlistInfo.name}** de **{playlistInfo.uploader}** a la cola! ({playlistInfo.totalVideos} canciones)")

        for song in songsArray:
            self.playlistDict[channelId].addSongToPlaylist(song)

        self.playlistDict[channelId].resumeCurrentSong()

        if not voiceClient.is_playing():
            await self.playSong(ctx, channelId)
            pass

    async def playSong(self, ctx, channelId = None) -> None:
        # this is a bit of a weird one
        # if the person who wrote the play command decides to leave the voice channel
        # then the context of the playing stops existing, thus it cant fetch the channel id.
        # passing the channel id as a parameter instead allows avoiding this thing
        # by not having to rely on a context which might stop existing at the time of query
        # if no channel is passed then it will be generated, and recursively usde without the
        # need for a context to even exist in the first place
        if channelId is None:
            channelId = ctx.author.voice.channel.id

        if channelId not in self.playlistDict:
            return
        
        playlist = self.playlistDict[channelId]
        if len(playlist.songList) == 0 or playlist.currentSongIndex >= len(playlist.songList):
            return
        
        voiceClient = None

        for voice_client in self.bot.voice_clients:
            if voice_client.channel and voice_client.channel.id == channelId:
                voiceClient = voice_client
                break

        if voiceClient.is_playing():
            print("Already playing something!")
            return
        
        song = playlist.getCurrentSong()

        await ctx.send(f"Reproduciendo: **{song.name}** - **{song.artist}** - {song.duration}")

        print('\n----------------------------------------------------------')

        try:
            audioStream = playlist.playCurrentSong()
        except ValueError:
            playlist.resetTimestamp()
            playlist.handleNextSong()
            await ctx.send("La canción no se encuentra disponible")
            await self.playSong(ctx, channelId)
            return

        voiceClient.play(audioStream)

        while voiceClient.is_playing() or voiceClient.is_paused() or playlist.isPlayingStopped:
            if voiceClient.is_paused() and (playlist.goingNext or playlist.goingPrev):
                break

            if playlist.isPlayingStopped and (playlist.goingNext or playlist.goingPrev):
                break

            if voiceClient.is_playing():
                playlist.addCountToTimestamp()

            await asyncio.sleep(1)

        playlist.resetTimestamp()
        playlist.handleNextSong()

        await self.playSong(ctx, channelId)

    async def searchByQuery(self, ctx, searchQuery : str, searchProvider : str = "Youtube") -> iStreamSong:
        channelId = ctx.author.voice.channel.id

        searchResults = self.playlistDict[channelId].getSongsBySearch(searchQuery, searchProvider)

        if len(searchResults) == 0:
            await ctx.reply("No hay resultados para tu búsqueda")
            return
        
        reply = "**RESULTADOS DE LA BÚSQUEDA:**\n"

        for i in range(len(searchResults)):
            song = searchResults[i]
            reply += f"{i+1}. {song.name} - {song.artist} - {song.duration}\n"

        reply += f"\nResponde a este mensaje con un numero del 1 al {len(searchResults)} para elegir una canción"

        await ctx.reply(reply)

        def check(message):
            return (
                message.author == ctx.author
                and message.channel == ctx.channel
                and message.content.isdigit()
                and 1 <= int(message.content) <= len(searchResults)
            )

        try:
            userResponse = await self.bot.wait_for("message", check = check, timeout = WAITING_TIMEOUT)
            chosenOption = int(userResponse.content) - 1
            return searchResults[chosenOption]

        except asyncio.TimeoutError:
            await ctx.send(f"Pasaron {WAITING_TIMEOUT} segundos y no elegiste nada tonto weon. Se canceló la solicitud")
            return None
        
        except ValueError:
            await ctx.send(f"Tienes que elegir un número del 1 al {len(searchResults)}")
            return None
        
    @music.command()
    async def pause(self, ctx):
        voiceClient = ctx.message.guild.voice_client

        if voiceClient and voiceClient.is_playing():
            voiceClient.pause()
            await ctx.send("Se pausó la canción")
        else:
            await ctx.send("No estaba sonando ninguna canción tonto weon.")
        
    @music.command()
    async def resume(self, ctx):
        voiceClient = ctx.message.guild.voice_client
        channelId = ctx.author.voice.channel.id

        if not voiceClient:
            await ctx.send("No estaba sonando ninguna canción tonto weon.")
            return
        
        if voiceClient.is_paused():
            voiceClient.resume()
            await ctx.send("Se resumió la canción")

        elif self.playlistDict[channelId].isPlayingStopped:
            self.playlistDict[channelId].resumeCurrentSong()
            voiceClient.resume()
            await ctx.send("Se resumió la canción")
            await self.playSong(ctx, channelId)
        
    @music.command()
    async def next(self, ctx):
        voiceClient = ctx.message.guild.voice_client
        channelId = ctx.author.voice.channel.id

        if not voiceClient:
            await ctx.send("No estoy conectado a ningun canal de voz tonto weon")
            return

        if not channelId:
            await ctx.send("No estas en un canal de voz tonto weon")
            return

        self.playlistDict[channelId].startGoingNextSong()
        voiceClient.stop()

        await ctx.reply("Saltando a la siguiente canción")

    @music.command()
    async def prev(self, ctx):
        voiceClient = ctx.message.guild.voice_client
        channelId = ctx.author.voice.channel.id

        if not voiceClient:
            await ctx.send("No estoy conectado a ningun canal de voz tonto weon")
            return

        if not channelId:
            await ctx.send("No estas en un canal de voz tonto weon")
            return

        self.playlistDict[channelId].startGoingPrevSong()

        if not voiceClient.is_playing() and not self.playlistDict[channelId].isPlayingStopped:
            self.playlistDict[channelId].handleNextSong()
            await self.playSong(ctx, channelId)

        voiceClient.stop()

        await ctx.reply("Retrocediendo a la anterior canción")

    @music.command()
    async def stop(self, ctx):
        voiceClient = ctx.message.guild.voice_client
        channelId = ctx.author.voice.channel.id

        if voiceClient is None:
            await ctx.reply("No estas conectado a un canal de voz tonto weon.")
            return

        if not voiceClient.is_playing():
            await ctx.send("No está sonando ninguna canción tonto weon.")
            return

        voiceClient.stop()
        self.playlistDict[channelId].stopCurrentSong()

        await ctx.reply("Se detuvo la reproducción de la canción")

    @music.command()
    async def clear(self, ctx):
        voiceClient = ctx.message.guild.voice_client
        channelId = ctx.author.voice.channel.id

        voiceClient.stop()
        self.playlistDict[channelId].stopCurrentSong()
        self.playlistDict[channelId].clearPlaylist()

        await ctx.reply("Se borraron todas las canciones de la cola")

    @music.command()
    async def queue(self, ctx):
        channelId=ctx.author.voice.channel.id
        reply = self.playlistDict[channelId].getCurrentPlaylist()
        await ctx.reply(reply)

    @music.group(invoke_without_command = True)
    async def loop(self, ctx):
        reply = "'c!music loop song' para iniciar loop de una sola cancion\n"
        reply += "'c!music loop playlist' para iniciar loop de toda la playlist"
        await ctx.reply(reply)

    @loop.command()
    async def song(self, ctx):
        voiceClient = ctx.message.guild.voice_client
        channelId = ctx.author.voice.channel.id

        if not voiceClient.is_playing():
            await ctx.reply("No hay ninguna cancion actualmente siendo reproducida")
            return

        looping = self.playlistDict[channelId].loopCurrentSong()
        if looping:
            await ctx.reply("Repitiendo la cancion actual!")
        else:
            await ctx.reply("Se desactivó la repetición de la canción actual")

    @loop.command()
    async def playlist(self, ctx):
        voiceClient = ctx.message.guild.voice_client
        channelId = ctx.author.voice.channel.id

        if not voiceClient.is_playing():
            await ctx.reply("No hay ninguna cancion actualmente siendo reproducida")
            return

        looping = self.playlistDict[channelId].loopPlaylist()
        if looping:
            await ctx.reply("Repitiendo la playlist!")
        else:
            await ctx.reply("Se desactivó la repetición de la playlist")

    @music.command()
    async def now(self, ctx):
        if not ctx.author.voice:
            await ctx.reply('No estas en un canal de voz tonto weon')
            return
        
        channel_id=ctx.author.voice.channel.id
        time = self.playlistDict[channel_id].getCurrentTimestamp()

        try:
            song = self.playlistDict[channel_id].getCurrentSong()

            progress = "LIVE"

            if song.duration != "LIVE":
                progress = SecondsToDurationFormatter.format(time)
                progress += f"/{song.duration}"

            reply = f"**Reproduciendo ahora:**\n"
            reply += f"**{song.name}** - **{song.artist}**\n"
            reply += f"Reproducción: {progress}"

            await ctx.reply(reply)
        except:
            reply = "No hay ninguna cancion en reproduccion ahora mismo"
            await ctx.reply(reply)

    @music.command()
    async def shuffle(self, ctx):
        channelId=ctx.author.voice.channel.id
        self.playlistDict[channelId].shufflePlaylist()
        await ctx.reply("La playlist ha sido randomizada!")

    @music.command()
    async def skip(self, ctx, arg):
        try:
            channelId = ctx.author.voice.channel.id
            voiceClient = ctx.message.guild.voice_client

            self.playlistDict[channelId].skipToIndex(arg, voiceClient.is_playing())
            
            await ctx.reply(f"Saltando a la canción {arg}...")
            await self.playSong(ctx, channelId)
            voiceClient.stop()

        except TypeError:
            await ctx.reply("El indice brindado es invalido!")

    @music.command()
    async def remove(self, ctx, arg):
        try:
            channelId = ctx.author.voice.channel.id
            self.playlistDict[channelId].removeIndex(arg)
            await ctx.reply(f"Se borró la cancíon {arg}!")
        except TypeError:
            await ctx.reply("El indice brindado es invalido!")
        except ValueError:
            await ctx.reply("La cancion esta sonando ahora mismo!")

musicCogInstance = MusicCog()