from typing import List

class StringSplitter:
    @staticmethod
    def split(text: str, maxCharacters: int) -> List[str]:
        wordsArray = text.split()
        splitString = [""]
        currentLine = 0

        for word in wordsArray:
            
            if len(splitString[currentLine]) + len(word) + 1 > maxCharacters:
                splitString.append("")
                currentLine += 1
                
            splitString[currentLine] += word + " "

        return splitString