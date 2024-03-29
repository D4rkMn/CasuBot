from bot.Utility.ImageDownloader import ImageDownloader
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import uuid
import os

from bot.Utility.StringSplitter import StringSplitter
from typing import List

mainPath = Path.cwd() / "momos"

inputPath = mainPath / "input"
outputPath = mainPath / "output"

watermarkPath = mainPath / "watermark.png"
fontPath = str(mainPath / "font.ttf")

class UrlTextPair:
    def __init__(self, _url : str, _text : str):
        self.url = _url
        self.text = _text

class MomoGenerator:

    @staticmethod
    def generate(*urlTextPairs):
        # each object is expected to be a tuple like (url,text)
        # such that they can be used to generating the momos
        # this explains the class UrlTextPair

        initialPath = MomoGenerator.__generateJoint(*urlTextPairs)

        if initialPath is None: # if momo generation failed
            return None

        finalPath = MomoGenerator.__addWatermark(initialPath)

        os.remove(initialPath)

        return finalPath

    @staticmethod
    def removeImageFromPath(path : Path) -> None:
        os.remove(path)

    @staticmethod
    def __generateJoint(*urlTextPairs):
        momoList = []
        pathList = []

        largestWidth = 0

        for pair in urlTextPairs:
            this_momo = MomoGenerator.__generateFromUrl(pair.url, pair.text)
        
            if this_momo is None: # if the image wasnt generated for some reason
                return None # return because it didnt work

            image = Image.open(this_momo)
            pathList.append(this_momo)

            largestWidth = max(largestWidth, image.size[0])
            momoList.append(image)

        result_path = MomoGenerator.__fuseMomos(momoList, largestWidth)

        for path in pathList:
            os.remove(path)

        return result_path

    @staticmethod
    def __addWatermark(path : Path) -> Path:
        image = Image.open(path)
        image = image.convert("RGBA")

        width, height = image.size

        watermark = Image.open(watermarkPath)
        watermark = watermark.resize((int(width // 4), int(width // 4))) 
        watermark = watermark.convert("RGBA")

        image.alpha_composite(watermark, (0, 2 * height // 5))

        result_path = outputPath / f"{str(uuid.uuid4())}.png"
        image.save(result_path)

        return result_path

    @staticmethod
    def __generateFromUrl(url : str, momoText : str) -> Path:
        imgPath = MomoGenerator.__downloadImageFromUrl(url)
        filePath = MomoGenerator.__generateMomoFromImage(imgPath, momoText)
        return filePath
    
    @staticmethod
    def __fuseMomos(momoList : List, largestWidth : float):
        finalHeight = 0

        for i in range(len(momoList)):
            momo = momoList[i]

            width, height = momo.size

            resize_factor = largestWidth / width
            new_height = int(height * resize_factor)

            momoList[i] = momo.resize((largestWidth, new_height))
            finalHeight += new_height
        
        finalImage = Image.new("RGB", (largestWidth, finalHeight), color = "white")    
        
        currentHeight = 0

        for momo in momoList:
            width, height = momo.size
            finalImage.paste(momo, (0, currentHeight))
            currentHeight += height

        filePath = outputPath / f"{str(uuid.uuid4())}.png"
        finalImage.save(filePath)

        return filePath

    @staticmethod
    def __downloadImageFromUrl(url : str) -> Path:
        filePath = inputPath / f"{str(uuid.uuid4())}.png"
        ImageDownloader.download(url, filePath)
        return filePath

    @staticmethod
    def __generateMomoFromImage(inputPath: Path, momoText: str) -> Path:
        if momoText.strip() == "":
            return None

        image = Image.open(inputPath)
        
        fontRatio = 0.1
        textColor = (0,0,0)

        width, height = image.size
        fontSize = int(min(width, height) * fontRatio)
        
        font = ImageFont.truetype(fontPath, fontSize)
        
        maxCharacters = int(width * 1.85 // fontSize)
        textLines = StringSplitter.split(momoText, maxCharacters)

        allocatedY = (len(textLines) + 1) * fontSize
        
        new_image = Image.new("RGBA", (width, height + allocatedY), color = "white")    
        draw = ImageDraw.Draw(new_image)

        new_image.paste(image, (0, allocatedY))

        textbox_val = draw.textbbox((0, 0), textLines[0], font = font)
        x_min, y_min, x_max, y_max = textbox_val
        line_height = y_max - y_min

        leftover_y = allocatedY - line_height * len(textLines)

        for i in range(len(textLines)):
            line=textLines[i]
            textbox_val = draw.textbbox((0, 0), line, font = font)
            x_min, y_min, x_max, y_max = textbox_val
            line_width = x_max - x_min

            line_x = (new_image.width - line_width) // 2
            line_y = (allocatedY - fontSize) / line_height + line_height * i + leftover_y//2

            draw.text((line_x, line_y), line, fill=textColor, font=font)        

        filePath = outputPath / f"{str(uuid.uuid4())}.png"
        new_image.save(filePath)

        os.remove(inputPath)
        return filePath