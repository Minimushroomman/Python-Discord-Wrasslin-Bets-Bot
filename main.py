# IMPORTS
# mySQL connecting
import mysql.connector
# mySQL error handling
from mysql.connector import Error
# Discord API
import discord
# logging
import logging
# Discord Bot API commands
from discord.ext import commands



# VARIABLES
# show database query in str
show_db_query = "SHOW DATABASES"

# database user name
db_username = "XXX"

# database password
db_pass = "XXX"

# name of db connecting to
db_name = "wrasslin_wednesday"

# token for discord bot
dc_token = 'XXX'

# description of what the bot does
description = 'A bot to track and place bets for Wrasslin Wednesday'

# intents - pulls default intents
intents = discord.Intents.default()

# establishes logging on file discord.log
logger = logging.getLogger('discord')
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

# IMPLEMENTING VARIABLES
# try connecting to mySQL database
try:
    mydb = mysql.connector.Connect(
        host="192.168.1.162",
        user=db_username,
        password=db_pass,
        database=db_name
    )
except Error as e:
    print(e)

# implement logging
logger.setLevel(logging.DEBUG)
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s'))
logger.addHandler(handler)

# Implement intents
intents.members = True
intents.messages = True

# Implement Bot
bot = commands.Bot(command_prefix=commands.when_mentioned_or('!'), description=description, intents=intents)


# start bot
try:
    bot.run(dc_token)
except Error as e:
    print(e)


# add a wrestler to database
def update_wrestler(name):
    insert_wrestler_query = """
    INSERT INTO wrestlers (name, wins, loss)
    VALUES
        ( {0}, 0, 0)
    """.format(name)
    print(insert_wrestler_query)
    with mydb.cursor() as cursor:
        cursor.execute(insert_wrestler_query)
        mydb.commit()


# return array of names
def get_wrestler_name():
    select_wrestler_name_query = "SELECT name FROM wrestlers"
    message = []
    with mydb.cursor() as cursor:
        cursor.execute(select_wrestler_name_query)
        for x in cursor.fetchall():
            message.append(list(x))
    return message


# return array of wins
def get_wrestler_wins():
    select_wrestler_wins_query = "SELECT wins FROM wrestlers"
    message = []
    with mydb.cursor() as cursor:
        cursor.execute(select_wrestler_wins_query)
        for x in cursor.fetchall():
            message.append(list(x))
    return message


# return array of losses
def get_wrestler_loss():
    select_wrestler_loss_query = "SELECT loss FROM wrestlers"
    message = []
    with mydb.cursor() as cursor:
        cursor.execute(select_wrestler_loss_query)
        for x in cursor.fetchall():
            message.append(list(x))
    return message


# return list of wrestlers
def get_wrestler_list():
    names = get_wrestler_name()
    wins = get_wrestler_wins()
    loss = get_wrestler_loss()
    message = "List of current wrestlers: "
    for x in range(len(names)):
        message = message + str(names[x]) + '(' + str(wins[x]) + ',' + str(loss[x]) + "), "
    return message


@bot.event
async def on_message(message):
    print('Message from {0.author}: {0.content}'.format(message))
    await bot.process_commands(message)


@bot.event
async def on_message(message):
    print("Message from {0.author}:{0}.content".format(message))
    await bot.process_commands(message)


@bot.command
async def wrestler(self, name):
    names = get_wrestler_name()
    if name in names:
        await self.send("Wrestler {0} is already added".format(name))
    else:
        update_wrestler(name)
        await self.send("{0} added to database! use !record to set their record.")



print(get_wrestler_list())
