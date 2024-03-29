from bot.Cogs.Help.iCommandHelp import iCommandHelp

class BirthdayHelp(iCommandHelp):
    @staticmethod
    def message() -> str:
        reply = """**AYUDA COMANDOS DE CUMPLEAÑOS:**:
- c!cum DD/MM: Establece tu propio cumpleaños
- c!cum list: Muestra la lista de fechas de cumpleaños
    """
        return reply