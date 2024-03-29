import openai

# import the base interface for the llm connector
from bot.Cogs.Chat.iLlmConnector import iLlmConnector

#
#   GptConnector
#   Implementation of iLlmConnector
#   Generates a response using ChatGPT's python package
#
class GptConnector(iLlmConnector):
    def __init__(self, _api_key : str, _maxTokens : int):
        openai.api_key = _api_key
        self.maxTokens = _maxTokens

    def generateResponse(self, inputText : str) -> str:
        response = openai.completions.create(
            model = "gpt-3.5-turbo-instruct",
            prompt = inputText,
            max_tokens= self.maxTokens
        )
        result = response.choices[0].text
        return result