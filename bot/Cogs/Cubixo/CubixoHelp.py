from bot.Cogs.Help.iCommandHelp import iCommandHelp

class CubixoHelp(iCommandHelp):
    @staticmethod
    def message() -> str:
        reply = """**AYUDA COMANDO CUBIXO:**
- c!cubixo <mensaje>: Dale un "mensaje" y responderá "SHoT_TheMEnSaJiXo"
(No se por que hice un apartado para cubixo porque a ver es un solo comando pero xd)
    """
        return reply