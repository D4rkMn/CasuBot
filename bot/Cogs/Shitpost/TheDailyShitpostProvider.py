import requests

# import the base interface for the shitpost provider
from bot.Cogs.Shitpost.iShitpostProvider import iShitpostProvider

STATUS_OK = 200

#
#   TheDailyShitpostProvider
#   Implementation of iShitpostProvider
#   Returns a shitpost from TheDailyShitpost database using its API
#
class TheDailyShitpostProvider(iShitpostProvider):
    def __init__(self):
        self.shitpostUrl = "https://api.thedailyshitpost.net/random"

    def getShitpost(self) -> str:
        response = requests.get(self.shitpostUrl)

        if response.status_code == STATUS_OK:
            json = response.json()
            result = json['url']
            return result
        
        raise SystemError("Internal server error")