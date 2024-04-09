from bot.Utility.DateFormatter import Date
from abc import ABC, abstractmethod
from typing import List

#
#   iReminderMessage
#   Interface to hold different implementations of reminder messages
#   Holds information about the reminder messages in the given database
#
class iReminderMessage(ABC):
    @property
    @abstractmethod
    def reminderId(self):
        pass

    @property
    @abstractmethod
    def serverId(self):
        pass

    @property
    @abstractmethod
    def channelId(self):
        pass

    @property
    @abstractmethod
    def messageReplyId(self):
        pass

    @property
    @abstractmethod
    def reminderContent(self):
        pass

    @property
    @abstractmethod
    def reminderDate(self):
        pass

#
#   iReminderDbConnector
#   Interface to hold different implementations of Database Connectors for the reminders cog
#
class iReminderDbConnector(ABC):
    @abstractmethod
    def addReminder(self, server_id : int, channel_id : int, reply_id : int, content : str, date : Date) -> None:
        pass
    
    @abstractmethod
    def getRemindersByServer(self, server_id : int) -> List[iReminderMessage]:
        pass

    @abstractmethod
    def removeReminder(self, reminder_id : int) -> None:
        pass