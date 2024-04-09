from sqlalchemy import create_engine, Column, Integer, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from typing import List

from bot.Cogs.Birthday.iBirthdayDbConnector import iBirthdayDbConnector, iServer, iMember

Base = declarative_base()

#
#   Server (for SQLAlchemy)
#   Implementation of iServer
#   Represents SQLite database relations for the server table via SQLAlchemy ORM
#
@iServer.register
class Server(Base):
    __tablename__ = "server"

    server_id = Column(Integer, primary_key = True)
    birthday_role_id = Column(Integer)
    birthday_channel_id = Column(Integer)

    members = relationship("Member", back_populates = "server")

    @property
    def serverId(self):
        return self.server_id

    @property
    def birthdayRoleId(self):
        return self.birthday_role_id
    
    @property
    def birthdayChannelId(self):
        return self.birthday_channel_id

#
#   Member (for SQLAlchemy)
#   Implementation of iMember
#   Represents SQLite database relations for the member table via SQLAlchemy ORM
#
@iMember.register
class Member(Base):
    __tablename__ = "member"

    user_id = Column(Integer, primary_key = True)
    server_id = Column(Integer, ForeignKey('server.server_id'), primary_key = True)
    birthday_day = Column(Integer, nullable = False)
    birthday_month = Column(Integer, nullable = False)

    server = relationship("Server", back_populates = "members")

    @property
    def userId(self):
        return self.user_id
    
    @property
    def serverId(self):
        return self.server_id
    
    @property
    def birthdayDay(self):
        return self.birthday_day
    
    @property
    def birthdayMonth(self):
        return self.birthday_month

#
#   BirthdaySQLiteConnector
#   Implementation of iBirthdayDbConnector
#   Connects to the birthdays SQLite database using SQLAlchemy ORM as a base
#
class BirthdaySQLiteConnector(iBirthdayDbConnector):
    def __init__(self):
        self.engine = create_engine("sqlite:///cums.db", echo = False)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind = self.engine)
        self.session = Session()

    def __del__(self):
        self.session.commit()
        self.session.close()

    def addServer(self, server_id : int) -> None:
        server = Server(server_id = server_id)
        try:
            self.session.add(server)
            self.session.commit()
        except:
            print("server already exists!")
            self.session.rollback()

    def addMember(self, user_id : int, server_id : int, birthday_day : int, birthday_month : int) -> None:
        member = Member(user_id = user_id, server_id = server_id, birthday_day = birthday_day, birthday_month = birthday_month)
        try:
            self.session.merge(member)
            self.session.commit()
        except Exception as e:
            print(f"adding member failed due to exception:\n{e}")
            self.session.rollback()

    def getAllServers(self) -> List[Server]:
        servers = self.session.query(Server).all()
        return servers

    def getServerById(self, server_id : int) -> Server:
        query = (
            self.session.query(Server)
            .filter_by(server_id = server_id)
        )
        server = query.first()
        return server

    def getMembersFromServer(self, server_id : int) -> List[Member]:
        query = (
            self.session.query(Member)
            .filter_by(server_id = server_id)
            .order_by(Member.birthday_month.asc(), Member.birthday_day.asc())
        )
        members = query.all()
        return members

    def setBirthdayChannel(self, server_id : int, channel_id : int) -> None:
        server = self.session.query(Server).filter_by(server_id = server_id).first()
        
        if not server:
            print("no server with such id found")
            return

        server.birthday_channel_id = channel_id
        self.session.commit()

    def setBirthdayRole(self, server_id : int, role_id : int) -> None:
        server = self.session.query(Server).filter_by(server_id = server_id).first()
        
        if not server:
            print("no server with such id found")
            return

        server.birthday_role_id = role_id
        self.session.commit()

    def removeMember(self, user_id : int) -> None:
        member = self.session.query(Member).filter_by(user_id = user_id).first()

        if not member:
            print("no member with such id found")
            return
        
        self.session.delete(member)
        self.session.commit()