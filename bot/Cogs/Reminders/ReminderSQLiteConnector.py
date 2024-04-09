from sqlalchemy import create_engine, Column, Integer, Text
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from typing import List

from bot.Utility.DateFormatter import Date
from bot.Cogs.Reminders.iReminderDbConnector import iReminderDbConnector, iReminderMessage

Base = declarative_base()

#
#   ReminderMessage (for SQLAlchemy)
#   Implementation of iReminderMessage
#   Represents SQLite database relations for the reminder table via SQLAlchemy ORM
#
@iReminderMessage.register
class ReminderMessage(Base):
    __tablename__ = "reminder"

    reminder_id = Column(Integer, primary_key = True, autoincrement = True)
    server_id = Column(Integer)
    channel_id = Column(Integer)
    reply_id = Column(Integer)
    content = Column(Text)
    reminder_day = Column(Integer)
    reminder_month = Column(Integer)

    @property
    def reminderId(self):
        return self.reminder_id

    @property
    def serverId(self):
        return self.server_id

    @property
    def channelId(self):
        return self.channel_id

    @property
    def messageReplyId(self):
        return self.reply_id

    @property
    def reminderContent(self):
        return self.content

    @property
    def reminderDate(self) -> Date:
        return Date(self.reminder_day, self.reminder_month)
    
#
#   ReminderSQLiteConnector
#   Implementation of iReminderDbConnector
#   Connects to the reminders SQLite database using SQLAlchemy ORM as a base
#
class ReminderSQLiteConnector(iReminderDbConnector):
    def __init__(self):
        self.engine = create_engine("sqlite:///reminders.db", echo = False)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind = self.engine)
        self.session = Session()

    def __del__(self):
        self.session.commit()
        self.session.close()

    def addReminder(self, server_id : int, channel_id : int, reply_id : int, content : str, date : Date) -> None:
        reminder = ReminderMessage(server_id = server_id, channel_id = channel_id,
            reply_id = reply_id, content = content, reminder_day = date.day, reminder_month = date.month)
        self.session.add(reminder)
        self.session.commit()
    
    def getRemindersByServer(self, server_id : int) -> List[ReminderMessage]:
        try:
            query = (
                self.session.query(ReminderMessage)
                .filter_by(server_id = server_id)
            )
            reminders = query.all()
            return reminders
        except:
            print("no server with such id found")
            return

    def removeReminder(self, reminder_id: int) -> None:
        member = self.session.query(ReminderMessage).filter_by(reminder_id = reminder_id).first()

        if not member:
            print("no reminder with such id found")
            return
        
        self.session.delete(member)
        self.session.commit()