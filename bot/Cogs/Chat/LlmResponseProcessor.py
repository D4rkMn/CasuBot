import re

class LlmResponseProcessor:
    @staticmethod
    def process(text : str) -> str:
        if '\n' in text:
            array = text.split('\n')
            text = LlmResponseProcessor.__getFirstNonEmpty(array)
        text = LlmResponseProcessor.__removeEmojis(text)
        return text
    
    @staticmethod
    def __getFirstNonEmpty(array):
        nonEmptyStrings = [s for s in array if s != '']
        return nonEmptyStrings[0] if nonEmptyStrings else None

    @staticmethod
    def __removeEmojis(text : str) -> str:
        # Define a regular expression pattern to match emojis
        emoji_pattern = re.compile("["
                                u"\U0001F600-\U0001F64F"  # emoticons
                                u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                u"\U00002500-\U00002BEF"  # chinese char
                                u"\U00002702-\U000027B0"
                                u"\U00002702-\U000027B0"
                                u"\U000024C2-\U0001F251"
                                u"\U0001f926-\U0001f937"
                                u"\U00010000-\U0010ffff"
                                u"\u2640-\u2642"
                                u"\u2600-\u2B55"
                                u"\u200d"
                                u"\u23cf"
                                u"\u23e9"
                                u"\u231a"
                                u"\ufe0f"  # dingbats
                                u"\u3030"
                                "]+", flags = re.UNICODE)
        # Replace emojis with an empty string
        cleaned_text = emoji_pattern.sub(r'', text)
        return cleaned_text