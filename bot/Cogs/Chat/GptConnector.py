from openai import OpenAI

# import the base interface for the llm connector
from bot.Cogs.Chat.iLlmConnector import iLlmConnector

#
#   GptConnector
#   Implementation of iLlmConnector
#   Generates a response using ChatGPT's python package
#
class GptConnector(iLlmConnector):
    def __init__(self, _api_key : str, _maxTokens : int):
        self.client = OpenAI(api_key = _api_key)
        self.maxTokens = _maxTokens

    def generateResponse(self, inputText : str) -> str:
        response = self.client.chat.completions.create(
            model = "gpt-4o-mini",
            messages = [{
                "role": "user",
                "content": [{
                    "type": "text",
                    "text": inputText
                }]
            }],
            response_format = {
                "type": "text"
            },
            temperature = 1.5,
            max_completion_tokens = self.maxTokens,
            top_p = 1,
            frequency_penalty = 0,
            presence_penalty = 0
        )
        result = response.choices[0].message.content
        return result