from bot.Cogs.Help.iCommandHelp import iCommandHelp

class ReminderHelp(iCommandHelp):
    @staticmethod
    def message() -> str:
        reply = """**AYUDA COMANDOS DE RECORDATORIO:**
- c!reminder DD/MM (mensaje): Establece un mensaje que quieres que el bot te recuerde
El mensaje será enviado de vuelta la próxima vez que se llegue a la fecha indicada. 
    """
        return reply