from bot.Utility.DateFormatter import DateFormatter, Date

from bot.Cogs.Reminders.iReminderDbConnector import iReminderDbConnector
from bot.Cogs.Reminders.ReminderSQLiteConnector import ReminderSQLiteConnector, iReminderMessage

from discord.ext import commands,tasks

#
#   ReminderCog
#   Cog implementation that contains bot commands related to the reminders database
#   Uses dependency injection to accept different database connectors if needed
#
class ReminderCog(commands.Cog):
    def __init__(self, _dbConnector : iReminderDbConnector):
        self.dbConnector = _dbConnector
        self.todayString = DateFormatter.todayAsString() # holds the current day. updates every 60 seconds
        self.prevDate = self.todayString # holds the previous value of todayString. for new day checking purposes

    def assignBot(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.todayString = DateFormatter.todayAsString()
        self.prevDate = self.todayString

        for server in self.bot.guilds:
            await self.checkForReminderDate(server.id)

        self.reminderNewDayCheck.start()

    @tasks.loop(seconds = 60)
    async def reminderNewDayCheck(self):
        self.prevDate = self.todayString
        self.todayString = DateFormatter.todayAsString()
        
        for server in self.bot.guilds:
            await self.checkForReminderDate(server.id)

    async def checkForReminderDate(self, server_id : int):
        todayDate = DateFormatter.todayAsDate()

        reminderArray = self.dbConnector.getRemindersByServer(server_id)

        for reminder in reminderArray:
            reminderDate = reminder.reminderDate
            if reminderDate.day == todayDate.day and reminderDate.month == todayDate.month:
                try:    
                    await self.sendReminder(reminder)
                    self.dbConnector.removeReminder(reminder.reminderId)
                except:
                    print("reminder couldnt be sent")

    async def sendReminder(self, reminder : iReminderMessage):
        server = self.bot.get_guild(reminder.serverId)
        channel = self.bot.get_channel(reminder.channelId)
        message = await channel.fetch_message(reminder.messageReplyId)
        await message.reply(reminder.reminderContent)

    @commands.command()
    async def reminder(self, ctx, arg : str = "", *, arg2 : str = ""):
        server_id = ctx.guild.id
        channel_id = ctx.channel.id
        reply_id = ctx.message.id
        user_id = ctx.author.id

        if arg2 == "":
            await ctx.reply("Debes añadir un mensaje para el recordatorio!")
            return

        if len(arg) != 5 or arg[2] != "/":
            await ctx.reply("Eso no es una fecha ah\n(Formato: 'DD/MM')")
            return

        try:
            reminder_day = int(arg[0:2])
            reminder_month = int(arg[3:5])
        except:
            await ctx.reply("Eso no es un cumpleaños ah\n(Formato: 'DD/MM')")
            return
        
        reminderDate = Date(reminder_day,reminder_month)

        self.dbConnector.addReminder(server_id, channel_id, reply_id, content = arg2, date = reminderDate)

        await ctx.reply(f"Recordatorio guardado! \n<@{user_id}>")

dbConnector = ReminderSQLiteConnector()
reminderCogInstance = ReminderCog(dbConnector)