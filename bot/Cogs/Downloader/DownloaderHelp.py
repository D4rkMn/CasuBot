from bot.Cogs.Help.iCommandHelp import iCommandHelp

class DownloadHelp(iCommandHelp):
    @staticmethod
    def message() -> str:
        reply = """**AYUDA COMANDOS DE DESCARGA:**
- c!download mp4 <url> <calidad>: Hace que el bot descargue el video a la calidad especificada
- c!download mp3 <url>: Hace que el bot descargue el audio del video
    """
        return reply