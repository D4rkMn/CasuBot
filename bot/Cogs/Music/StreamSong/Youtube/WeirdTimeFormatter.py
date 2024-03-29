from datetime import timedelta

#
#   WeirdTimeFormatter
#   YT's api has a weird format for duration. Something like "PT2M43S"? This things turns that into actually readable shit
#
class WeirdTimeFormatter:
    @staticmethod
    def format(duration_str : str) -> str:
        duration_str = duration_str[2:]
        duration = timedelta()
        if 'H' in duration_str:
            duration += timedelta(hours=int(duration_str.split('H')[0]))
            duration_str = duration_str.split('H')[1]
        if 'M' in duration_str:
            duration += timedelta(minutes=int(duration_str.split('M')[0]))
            duration_str = duration_str.split('M')[1]
        if 'S' in duration_str:
            duration += timedelta(seconds=int(duration_str.split('S')[0]))

        hours, remainder = divmod(duration.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)

        if hours != 0:
            return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
        
        if minutes >= 10:
            return f"{int(minutes):02d}:{int(seconds):02d}"
        
        else:
            return f"{int(minutes):01d}:{int(seconds):02d}"