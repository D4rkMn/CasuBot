from openai import OpenAI
from bot.Cogs.Chat.iLlmConnector import Message

def getStringFromFile(filename : str) -> str:
    result = ""
    with open(filename) as f: 
        for line in f.readlines():
            result += line
    return result

def getSystemMessage() -> str:
    prefix = "bot/Cogs/Chat/SystemMessages/"
    return getStringFromFile(prefix + "ImageAnalizer.txt")

#
#   UserResponseProcessor
#   Processes a user response to get it to not contain images anymore
#
class UserResponseProcessor:
    def __init__(self, _api_key : str, _maxTokens : int):
        self.systemMessage = {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": getSystemMessage()
                }
            ]
        }
        self.client = OpenAI(api_key = _api_key)
        self.maxTokens = _maxTokens

    def process(self, message : Message) -> Message:
        messageList = [ self.systemMessage ]
        for imageUrl in message.imagesArray:
            item = {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": imageUrl
                        }
                    }
                ]
            }
            messageList.append(item)
        response = self.__gptProcess(messageList)

        message.imagesArray.clear()
        message.textArray.append(response)
        return message

    def __gptProcess(self, messageList) -> str:
        response = self.client.chat.completions.create(
            model = "gpt-4o-mini",
            messages = messageList,
            response_format = {
                "type": "text"
            },
            temperature = 1,
            max_completion_tokens = self.maxTokens,
            top_p = 1,
            frequency_penalty = 0,
            presence_penalty = 0
        )
        result = response.choices[0].message.content
        return result