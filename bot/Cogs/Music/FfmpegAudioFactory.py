from discord import FFmpegPCMAudio
from io import BufferedIOBase

FFMPEG_OPTS = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"

#
#   FfmpegAudioFactory
#   Factory that creates FFmpegPCMAudio types for different types of audio sources
#
class FfmpegAudioFactory:
    @staticmethod
    def create(source : str | BufferedIOBase, pipe: bool = False) -> FFmpegPCMAudio:
        if pipe:
            return FFmpegPCMAudio(source = source, pipe = True)
        return FFmpegPCMAudio(source = source, before_options = FFMPEG_OPTS)