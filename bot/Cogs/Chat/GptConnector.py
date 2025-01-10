from openai import OpenAI

# import the base interface for the llm connector
from bot.Cogs.Chat.iLlmConnector import iLlmConnector, Message
from typing import List

#
#   GptConnector
#   Implementation of iLlmConnector
#   Generates a response using ChatGPT's python package
#
class GptConnector(iLlmConnector):
    def __init__(self, _api_key : str, _maxTokens : int):
        self.client = OpenAI(api_key = _api_key)
        self.maxTokens = _maxTokens

    def generateResponse(self, systemMessage : Message, chatlog : List[Message]) -> str:
        messageList = self.generateMessageList(systemMessage, chatlog)
        response = self.client.chat.completions.create(
            model = "gpt-4o-mini",
            messages = messageList,
            response_format = {
                "type": "text"
            },
            temperature = 1.15,
            max_completion_tokens = self.maxTokens,
            top_p = 1,
            frequency_penalty = 0,
            presence_penalty = 0
        )
        result = response.choices[0].message.content
        return result
    
    def processMessage(self, message : Message):
        role = ""
        if message.username == "Sistema":
            role = "system"
        elif message.username == "Casu":
            role = "assistant"
        else:
            role = "user"
        
        messageContent = []
        
        for textContent in message.textArray:
            messageContent.append({
                "type": "text",
                "text": f"{message.username}: {textContent}"
            })

        for imageUrl in message.imagesArray:
            messageContent.append({
                "type": "image_url",
                "image_url": {
                    "url": imageUrl
                }
            })

        return {
            "role": role,
            "content": messageContent
        }