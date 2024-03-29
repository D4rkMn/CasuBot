from bot.Utility.ImageDownloader import ImageDownloader
from pathlib import Path
from PIL import Image
import uuid
import os

mainPath = Path.cwd() / "globo"
downloadPath = mainPath / "downloads"
resultPath = mainPath / "results"

bubblePath = mainPath / "globo.png"
bubbleImage = Image.open(bubblePath)

class SpeechBubbleGenerator:
    
    @staticmethod
    def generateFromUrl(url : str) -> Path:
        imgPath = SpeechBubbleGenerator.__downloadImageFromUrl(url)
        filePath = SpeechBubbleGenerator.__addSpeechBubbleToImage(imgPath)
        return filePath

    @staticmethod
    def removeImageFromPath(path : Path) -> None:
        os.remove(path)

    @staticmethod
    def __downloadImageFromUrl(url : str) -> Path:
        filePath = downloadPath / f"{str(uuid.uuid4())}.png"
        ImageDownloader.download(url, filePath)
        return filePath

    @staticmethod
    def __addSpeechBubbleToImage(path : Path) -> Path:
        img=Image.open(path)

        tempBubble = bubbleImage.resize(
            (img.width, int(bubbleImage.height * img.width / bubbleImage.width))
        )

        result = Image.new("RGB", (tempBubble.width, tempBubble.height + img.height))
        result.paste(tempBubble, (0,0))
        result.paste(img, (0, tempBubble.height))

        filePath = resultPath / f"{str(uuid.uuid4())}.gif"
        result.save(filePath)

        os.remove(path)
        return filePath