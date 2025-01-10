from discord import message
from typing import List

#
#   ImageUrlExtractor
#   Extracts url's from a given message (assuming it has an image embedded somehow). If not then raises error
#
class ImageUrlExtractor:
    
    @staticmethod
    def extract(message : message) -> str:
        if len(message.embeds) > 0:
            embed = message.embeds[0]

            if embed.thumbnail and embed.thumbnail.url:
                return embed.thumbnail.url
            if embed.image and embed.image.url:
                return embed.image.url
            if embed.url:
                return embed.url

        if len(message.attachments) > 0:
            attachment = message.attachments[0]
            if attachment.content_type and attachment.content_type.startswith("image/"):
                return attachment.url
        
        return None
        
    @staticmethod
    def extractAll(message : message) -> List[str]:
        imageUrls = []

        if len(message.embeds) > 0:
            for embed in message.embeds:
                # Check and add thumbnail URL
                if embed.thumbnail and embed.thumbnail.url:
                    imageUrls.append(embed.thumbnail.url)
                
                # Check and add main image URL
                if embed.image and embed.image.url:
                    imageUrls.append(embed.image.url)
                
                # Check and add embed URL if it contains an image
                if embed.url:
                    imageUrls.append(embed.url)

        # Extract images from attachments
        if len(message.attachments) > 0:
            for attachment in message.attachments:
                # Only include attachments that are images
                if attachment.content_type and attachment.content_type.startswith("image/"):
                    imageUrls.append(attachment.url)
        
        return imageUrls