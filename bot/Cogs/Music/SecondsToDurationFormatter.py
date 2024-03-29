#
#   SecondsToDurationFormatter
#   Formats integer time seconds to a time duration string 
#
class SecondsToDurationFormatter:
    @staticmethod
    def format(time : int) -> str:
        hours = time // 3600
        minutes = time // 60
        seconds = time % 60

        mm = str(minutes)
        ss = str(seconds)

        if len(ss) != 2:
            ss = f"0{ss}"

        if hours != 0:
            if len(mm) != 2:
                mm = f"0{mm}"

            return f"{hours}:{mm}:{ss}"
            
        return f"{mm}:{ss}"