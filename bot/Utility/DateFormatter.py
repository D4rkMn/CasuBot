from datetime import date

#
#   Date
#   Acts as a pair for day and month
#
class Date:
    def __init__(self, _day : int, _month : int):
        self.day = _day
        self.month = _month

#
#   DateFormatter
#   Gets the current date, formats it and returns it
#
class DateFormatter:
    @staticmethod
    def todayAsString() -> str:
        return date.today().strftime("%d/%m/%Y")[:-5]

    @staticmethod
    def todayAsDate() -> Date:
        todayString = DateFormatter.todayAsString()
        day = int(todayString[0:2])
        month = int(todayString[3:5])
        return Date(day, month)