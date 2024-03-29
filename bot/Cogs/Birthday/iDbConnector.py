from abc import ABC, abstractmethod
from typing import List

#
#   iServer
#   Interface to hold different implementations of servers
#   Holds information about the servers in the given database
#
class iServer(ABC):
    @property
    @abstractmethod
    def serverId(self):
        pass

    @property
    @abstractmethod
    def birthdayRoleId(self):
        pass

    @property
    @abstractmethod
    def birthdayChannelId(self):
        pass

#
#   iMember
#   Interface to hold different implementations of members
#   Holds information about the members in the given database
#
class iMember(ABC):
    @property
    @abstractmethod
    def userId(self):
        pass

    @property
    @abstractmethod
    def serverId(self):
        pass

    @property
    @abstractmethod
    def birthdayDay(self):
        pass

    @property
    @abstractmethod
    def birthdayMonth(self):
        pass

#
#   iDbConnector
#   Interface to hold different implementations of Database Connectors 
#
class iDbConnector(ABC):
    @abstractmethod
    def addServer(self, server_id : int) -> None:
        pass

    @abstractmethod
    def addMember(self, user_id : int, server_id : int, birthday_day : int, birthday_month : int) -> None:
        pass

    @abstractmethod
    def getAllServers(self) -> List[iServer]:
        pass

    @abstractmethod
    def getServerById(self, server_id : int) -> iServer:
        pass

    @abstractmethod
    def getMembersFromServer(self, server_id : int) -> List[iMember]:
        pass

    @abstractmethod
    def setBirthdayChannel(self, server_id : int, channel_id : int) -> None:
        pass

    @abstractmethod
    def setBirthdayRole(self, server_id : int, role_id : int) -> None:
        pass

    @abstractmethod
    def removeMember(self, user_id : int) -> None:
        pass