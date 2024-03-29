from discord import message

#
#   ImageUrlExtractor
#   Extracts url's from a given message (assuming it has an image embedded somehow). If not then raises error
#
class ImageUrlExtractor:
    
    @staticmethod
    def extract(message : message):
        if len(message.embeds)>0:
            embed=message.embeds[0]

            if embed.thumbnail.url is not None:
                return embed.thumbnail.url
            elif embed.url is not None:
                return embed.url
            else:
                return embed.image.url

        elif len(message.attachments)>0:
            embed=message.attachments[0]
            return embed.url
        
        else:
            return None