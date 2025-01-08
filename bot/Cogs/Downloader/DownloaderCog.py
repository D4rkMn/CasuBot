from discord.ext import commands
from discord.errors import HTTPException
from discord import File
from bot.Cogs.Downloader.VideoDownloader import VideoDownloader

#
#   DownloaderCog
#   Cog implementation that contains bot commands to download videos
#
class DownloaderCog(commands.Cog):
    def assignBot(self, bot):
        self.bot = bot

    @commands.group()
    async def download(self, ctx):
        pass

    @download.command()
    async def mp4(self, ctx, url : str = "", qualityString : str = ""):
        if url == "":
            await ctx.reply("Donde esta el video?\nSe fue\nSE FUEEEEEEEEEEE")
            return

        if qualityString == "":
            await ctx.reply("Debes especificar una calidad de video!")
            return
        
        if not VideoDownloader.checkIfValidQuality(qualityString):
            await ctx.reply("La calidad ingresada no es valida!")
            return
        
        await ctx.send("Descargando...")
        quality = int(qualityString)

        try:
            videoPath = VideoDownloader.downloadYTVideoByUrl(url, quality)
            with open(videoPath, "rb") as file:
                result = File(file)
                await ctx.reply(file = result)

        # fallback option. just in case
        except ValueError:
            await ctx.reply("La calidad ingresada no es valida!")

        except HTTPException:
            await ctx.reply("El video especificado a descargar es muy pesado!")

        except Exception as e:
            await ctx.reply("El video no se pudo descargar por motivos (?")
            await ctx.send(f"El cliente respondió con: {e}")
            print(type(e))

        finally:
            try:
                VideoDownloader.removeFileFromPath(videoPath)
            except:
                pass

    @download.command()
    async def mp3(self, ctx, url : str = ""):
        if url == "":
            await ctx.reply("Donde esta el video?\nSe fue\nSE FUEEEEEEEEEEE")
            return
        
        await ctx.send("Descargando...")

        try:
            videoPath = VideoDownloader.downloadYTAudioByUrl(url)
            with open(videoPath, "rb") as file:
                result = File(file)
                await ctx.reply(file = result)

        except HTTPException:
            await ctx.reply("El video especificado a descargar es muy pesado!")

        except Exception as e:
            await ctx.reply("El video no se pudo descargar por motivos (?")
            await ctx.send(f"El cliente respondió con: {e}")
            
        finally:
            try:
                VideoDownloader.removeFileFromPath(videoPath)
            except:
                pass

downloaderCogInstance = DownloaderCog()