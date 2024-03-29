from pathlib import Path
import requests

STATUS_OK = 200

class ImageDownloader:

    @staticmethod
    def download(url, path : Path) -> None:
        if url is None:
            print("invalid url")
            return
        
        result = requests.get(url)

        if result.status_code != STATUS_OK:
            print("error when fetching url")
            return

        path.write_bytes(result.content)