from bot.Cogs.Help.iCommandHelp import iCommandHelp

class UpdatesHelp(iCommandHelp):
    @staticmethod
    def message() -> str:
        reply = """**AYUDA COMANDOS DE UPDATES:**
- c!updates changelog: Muestra los últimos cambios hechos al bot
- c!updates todo: Muestra una lista de actualizaciones pendientes para el bot
    """
        return reply