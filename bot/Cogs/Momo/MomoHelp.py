from bot.Cogs.Help.iCommandHelp import iCommandHelp

class MomoHelp(iCommandHelp):
    @staticmethod
    def message() -> str:
        reply = """**AYUDA COMANDO MOMO:**
- c!momo "texto 1" "texto 2" "texto 3" ...
Tambien debes añadir imagenes a tu mensaje para que se puedan usar como plantillas para el momo. Se harán tantas viñetas como imagenes hayas añadido.
"""
        return reply