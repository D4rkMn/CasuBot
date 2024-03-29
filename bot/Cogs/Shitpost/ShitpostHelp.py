from bot.Cogs.Help.iCommandHelp import iCommandHelp
from bot.Cogs.Shitpost.ShitpostCog import shitpostRNG

class ShitpostHelp(iCommandHelp):
    @staticmethod
    def message() -> str:
        reply = f"""**AYUDA COMANDOS DE SHITPOST:**
- c!shitpost: Hace que el bot envíe un video random de una colección enorme de videos
- dato extra: El bot enviará un shitpost al azar (con una probabilidad de 1 en {shitpostRNG})
- otro dato extra: La coleccion de videos no le pertenece a Jano, asi que no le cuestionen si sale algo raro, el tarado tampoco tiene ni idea 
    """
        return reply