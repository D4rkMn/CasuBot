from bot.Cogs.Help.iCommandHelp import iCommandHelp

class ChatHelp(iCommandHelp):
    @staticmethod
    def message() -> str:
        reply = """**AYUDA COMANDO CHAT:**
Bueno, esto realmente no es un comando, pero igual tiene sus reglas, por asi decirlo.
Si le haces ping a casu (@casu), o le respondes (enviandole notificacion de todas formas),
casu te responderá (mediante un personaje llevado por un Large Language Model, como ChatGPT).
Nada de lo que te responda o no casu tiene que ver con las opiniones de jano, así que no le pregunten.
"""
        return reply