from pathlib import Path
import yt_dlp
import uuid
import os
import re

mainPath = Path.cwd() / "videos"
outputPath = mainPath / "output"

ACCEPTED_QUALITIES = [144, 360, 480, 720, 1080]

class VideoDownloader:
    @staticmethod
    def downloadYTVideoByUrl(url : str, quality : int) -> str:
        _uuid = str(uuid.uuid4())
        try:
            options = VideoDownloader.__getYTVideoOpts(quality, _uuid)
            with yt_dlp.YoutubeDL(options) as ydl:
                url = VideoDownloader.__parseYTUrl(url)
                code = ydl.download([url])
            return f"{outputPath}/{_uuid}" + ".mp4"
                
        except yt_dlp.DownloadError:
            raise BrokenPipeError("Failed to download file!")
        
        # if invalid given quality
        except ValueError as e:
            raise ValueError(e)
        
    @staticmethod
    def downloadYTAudioByUrl(url : str) -> str:
        try:
            _uuid = str(uuid.uuid4())
            options = VideoDownloader.__getYTAudioOpts(_uuid)
            with yt_dlp.YoutubeDL(options) as ydl:
                url = VideoDownloader.__parseYTUrl(url)
                code = ydl.download([url])
            return f"{outputPath}/{_uuid}" + ".mp3"
                
        except yt_dlp.DownloadError:
            raise BrokenPipeError("Failed to download file!")
        
    @staticmethod
    def removeFileFromPath(filePath : str) -> None:
        os.remove(filePath)

    @staticmethod
    def checkIfValidQuality(quality : str) -> bool:
        try:
            _quality = int(quality)
            return _quality in ACCEPTED_QUALITIES
        except:
            return False

    @staticmethod
    def __getYTVideoOpts(quality : int, filename : str):
        if quality not in ACCEPTED_QUALITIES:
            raise ValueError("That quality option isnt valid!")

        return {
            "format_sort": [f"res:{quality}", "ext:mp4:m4a"],
            "outtmpl" : f"{outputPath}/{filename}" + ".%(ext)s",
            "noplaylist" : True
        }
    
    @staticmethod
    def __getYTAudioOpts(filename : str):
        return {
            "format" : "bestaudio",
            "force_generic_extractor" : True,
            "noplaylist" : True,
            "postprocessors" : [{
                "key" : "FFmpegExtractAudio",
                "preferredcodec" : "mp3",
                "preferredquality" : "192"
            }],
            "outtmpl" : f"{outputPath}/{filename}" + ".%(ext)s",
        }
    
    @staticmethod
    def __parseYTUrl(url : str):
        # Regex pattern to match the playlist section in the URL
        pattern = r'&list=[^&]+'
        # Replace the matched pattern with an empty string
        cleaned_url = re.sub(pattern, '', url)
        return cleaned_url