from bot.Cogs.Help.iCommandHelp import iCommandHelp

class MusicHelp(iCommandHelp):
    @staticmethod
    def message() -> str:
        reply = """**AYUDA COMANDOS DE MÚSICA:**
- c!music join: Hace que el bot se una a tu canal de voz
- c!music leave: Hace que el bot deje el canal de voz (este comando vacía la cola de canciones)
- c!music play <keywords>: Hace que el bot devuelva los primeros 10 resultados de busqueda, y el que se elija se añadirá
- c!music play <url>: Añade el url a la cola. Actualmente soporta Youtube, Spotify y links de Discord
- c!music play (subir archivo): Hace que el bot añada el archivo (mp3 o mp4) a la cola
- c!music search (yt|sp) <keywords>: Hace que el bot devuelva los primeros 10 resultados de busqueda. Actualmente puedes buscar en Youtube (yt) o en Spotify (sp)
- c!music pause: Pausa la canción. Puede ser resumida con c!music resume
- c!music stop: Detiene la canción y reinica la reproducción
- c!music resume: Resume la canción si fue pausada. Si fue detenida, se reiniciará
- c!music queue: Devuelve la cola de reproducción entera. En **negrita** se mostrará la canción actual
- c!music now: Devuelve información sobre la reproducción actual
- c!music next: Reproduce la siguiente canción en cola
- c!music prev: Reproduce la anterior canción en cola
- c!music skip <numero>: Salta a la canción con el número correspondiente
- c!music remove <numero>: Elimina la canción con el número correspondiente
- c!music loop song: Repite la cancion actual en lugar de pasar a la siguiente
- c!music loop playlist: Repite la cola de canciones actual cuando se acaben las canciones
- c!music shuffle: Randomiza la lista de canciones a un orden aleatorio
    """
        return reply