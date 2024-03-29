import validators

class UrlValidator:
    @staticmethod
    def check(string : str) -> bool:
        return validators.url(string) == True