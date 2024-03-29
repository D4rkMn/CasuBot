from bot.Cogs.Help.iCommandHelp import iCommandHelp

class GloboHelp(iCommandHelp):
    @staticmethod
    def message() -> str:
        reply = """**AYUDA COMANDO GLOBO:**
- c!globo: Genera un globo de texto en base a una imagen
Este comando tiene unas cuantas especificaciones.
Si el comando que invoca al bot TIENE una imagen, la imagen que se globeará será esa.
Si el comando NO TIENE una imagen, la imagen a ser globeada sera diferente en base a:
Si el comando RESPONDE a una imagen, la imagen globeada sera la imagen de la respuesta.
Si el comando NO RESPONDE a nada, la imagen globeada sera la ultima imagen que se pueda encontrar entre los ultimos 100 mensajes.
"""
        return reply