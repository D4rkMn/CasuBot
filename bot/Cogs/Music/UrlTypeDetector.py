#
#   UrlTypeDetector
#   Class that detects if a url corresponds to a youtube url, spotify url, etc
#
class UrlTypeDetector:
    @staticmethod
    def detect(url : str) -> str:
        if UrlTypeDetector.__urlIsWebsiteOf(url, "www.youtube.com") or UrlTypeDetector.__urlIsWebsiteOf(url, "youtube.be") or UrlTypeDetector.__urlIsWebsiteOf(url, "youtube.com"):
            return "Youtube"
        elif UrlTypeDetector.__urlIsWebsiteOf(url, "open.spotify.com"):
            return "Spotify"
        elif UrlTypeDetector.__urlIsWebsiteOf(url, "cdn.discordapp.com"):
            return "File"
        
    @staticmethod
    def __urlIsWebsiteOf(mainUrl : str, comparedUrl : str) -> bool:
        return mainUrl.startswith(f"https://{comparedUrl}") or mainUrl.startswith(f"http://{comparedUrl}")