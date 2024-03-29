from bot.Cogs.Help.iCommandHelp import iCommandHelp

class TalkHelp(iCommandHelp):
    @staticmethod
    def message() -> str:
        reply = """**AYUDA COMANDOS DE HABLAR:**
- c!talk (mensaje): Hace que el bot repita el mensaje
¿En serio? Que clase de funcion de mierda es esta.
    """
        return reply