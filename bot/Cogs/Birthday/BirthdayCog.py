from bot.Cogs.Birthday.DateFormatter import DateFormatter, Date

from bot.Cogs.Birthday.iDbConnector import iDbConnector
from bot.Cogs.Birthday.SQLiteConnector import SQLiteConnector, iServer, iMember

from discord.ext import commands,tasks
from discord import utils, AllowedMentions

#
#   BirthdayCog
#   Cog implementation that contains bot commands related to the birthday database
#   Uses dependency injection to accept different database connectors if needed
#
class BirthdayCog(commands.Cog):
    def __init__(self, _dbConnector : iDbConnector):
        self.dbConnector = _dbConnector
        self.months = "enero febrero marzo abril mayo junio julio agosto septiembre octubre noviembre diciembre".split()
        
        self.todayString = DateFormatter.todayAsString() # holds the current day. updates every 60 seconds
        self.prevDate = self.todayString # holds the previous value of todayString. for new day checking purposes
        self.greetedForToday = True # wishing happy birthday only happens once a day. this ensures this will be the case

    def assignBot(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.todayString = DateFormatter.todayAsString()
        self.prevDate = self.todayString

        serverArray = self.dbConnector.getAllServers()
        
        for server in serverArray:
            await self.wishHappyBirthday(server.serverId)

        self.newDayCheck.start()

    @tasks.loop(seconds = 60)
    async def newDayCheck(self):
        self.prevDate = self.todayString
        self.todayString = DateFormatter.todayAsString()

        self.greetedForToday = (self.todayString != self.prevDate)

        if not self.greetedForToday:
            return
        
        # opt instead for checking the bots cache rather than querying the database every minute
        for server in self.bot.guilds:
            await self.wishHappyBirthday(server.id)

    async def wishHappyBirthday(self, serverId : int) -> None:
        server = self.bot.get_guild(serverId)
        # if not in cache
        if not server:
            try:
                server = await self.bot.fetch_guild(serverId)
            except:
                print(f"server with id {serverId} is dead (?)")
                return
        
        serverDbObject : iServer = self.dbConnector.getServerById(serverId)

        if not serverDbObject:
            print(f"server {server} is not set up correctly")
            return
        
        roleToAssign = utils.get(server.roles, id = serverDbObject.birthdayRoleId)
        greetingChannel = self.bot.get_channel(serverDbObject.birthdayChannelId)

        if roleToAssign is None or greetingChannel is None:
            if roleToAssign is None:
                print(f"server {server} has no set birthday role")
            if greetingChannel is None:
                print(f"server {server} has no set birthday channel")
            return
        
        todayDate = DateFormatter.todayAsDate()

        memberArray = self.dbConnector.getMembersFromServer(serverId)

        for member in memberArray:
            memberUser = server.get_member(member.userId)

            try:

                if member.birthdayDay == todayDate.day and member.birthdayMonth == todayDate.month:
                    self.greetedForToday = False

                    if roleToAssign in memberUser.roles:
                        print(f"user {memberUser} has already been given the birthday role")
                        continue

                    allowedMentions = AllowedMentions(everyone = True)
                    message = f"Hoy es el cumpleaños del tarado de <@{member.userId}> . Saludenlo o lo que sea @everyone"
                    await greetingChannel.send(message, allowed_mentions = allowedMentions)
                    await memberUser.add_roles(roleToAssign)

                else:
                    await memberUser.remove_roles(roleToAssign)

            except:
                
                print(f"member {member.userId} from server {server} is dead (?")

    @commands.command()
    async def cum(self, ctx, arg : str = "", arg2 : str = ""):
        server_id = ctx.guild.id
        user_id = ctx.author.id

        if arg == "list":
            await self.listBirthdays(ctx, server_id)
            return
        
        if arg == "":
            await ctx.reply("Ayuda sobre el comando con c!help cum")
            return
        
        if arg2 != "" or len(arg) != 5 or arg[2] != "/":
            await ctx.reply("Eso no es un cumpleaños ah\n(Formato: 'DD/MM')")
            return

        try:
            birthday_day = int(arg[0:2])
            birthday_month = int(arg[3:5])
        except:
            await ctx.reply("Eso no es un cumpleaños ah\n(Formato: 'DD/MM')")
            return

        self.dbConnector.addServer(server_id)
        self.dbConnector.addMember(user_id, server_id, birthday_day, birthday_month)

        await ctx.reply(f"Fecha guardada! \n<@{user_id}>")

    # admin only commands
    @commands.group(invoke_without_command = True)
    @commands.has_permissions(administrator = True)
    async def cum_admin(self, ctx):
        reply = "c!cum_admin channel: To set birthday channel\n"
        reply += "c!cum_admin role: To set birthday role"
        await ctx.reply(reply)

    @cum_admin.command()
    @commands.has_permissions(administrator = True)
    async def channel(self, ctx) -> None:
        serverId = ctx.guild.id
        channelId = ctx.channel.id
        self.dbConnector.addServer(serverId)
        self.dbConnector.setBirthdayChannel(serverId, channelId)
        await ctx.reply("Se estableció correctamente el canal de cumpleaños!")

    # for this one you have to ping the role you want to add
    @cum_admin.command()
    @commands.has_permissions(administrator = True)
    async def role(self, ctx, rolePing) -> None:
        serverId = ctx.guild.id
        try:
            roleId = self.pingToId(rolePing)
            self.dbConnector.addServer(serverId)
            self.dbConnector.setBirthdayRole(serverId, roleId)
            await ctx.reply("Se estableció correctamente el rol de cumpleaños!")
        except TypeError:
            await ctx.reply("El argumento del comando no es un rol")

    # allows you to add a user without them having to run the command
    @cum_admin.command()
    @commands.has_permissions(administrator = True)
    async def add(self, ctx, userId : str, dateString : str) -> None:
        serverId = ctx.guild.id
        try:
            userId = int(userId)
            birthday_day = int(dateString[0:2])
            birthday_month = int(dateString[3:5])
            self.dbConnector.addServer(serverId)
            self.dbConnector.addMember(userId, serverId, birthday_day, birthday_month)
        except:
            print(f"exception in cum admin add: {userId}, {serverId}")

    async def listBirthdays(self, ctx, server_id : int):
        reply = await self.listBirthdaysFromServer(server_id)
        await ctx.reply(reply)

    async def listBirthdaysFromServer(self, server_id : int) -> str:
        memberArray = self.dbConnector.getMembersFromServer(server_id)

        reply = "**LISTA DE FECHAS DE CUMPLEAÑOS:**\n"

        for member in memberArray:
            try:
                user = await self.bot.fetch_user(member.userId)
            except:
                continue
            username = user.name
            spacing = " " * (32 - len(username)) # generate empty spaces from the usernames length

            line = f"**{username}** :{spacing}{member.birthdayDay} de {self.months[member.birthdayMonth - 1]}\n"
            reply += line.format()

        return reply
    
    def pingToId(self, ping : str) -> int:
        try:
            if ping[2] == "&":
                ping = ping[3:-1]
            else:
                ping = ping[2:-1]
            return int(ping)
        except:
            raise TypeError("Not a ping")

dbConnector = SQLiteConnector()
birthdayCogInstance = BirthdayCog(dbConnector)