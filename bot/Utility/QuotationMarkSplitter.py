import re
from typing import List

class QuotationMarkSplitter:
    @staticmethod
    def split(text : str) -> List[str]:
        # Use regex to find all text within quotation marks
        sentences = re.findall(r'"(.*?)"', text)
        return sentences