import os
import discord
import logging
from replit import db
from discord.ext import commands



#VARIABLES
#pulls bot token, provided by discord from enviorment variables
token = os.environ['TOKEN']
#description of what the bot does
description = 'A bot to track and place bets for Wrasslin Wednesday'
#intents - pulls default intetnts
intents = discord.Intents.default()
#establishes logging on file discord.log
logger = logging.getLogger('discord')
handler = logging.FileHandler(filename='discord.log', encoding= 'utf-8', mode='w')
#error message for an empty database
empty = "No wrestlers found in database"

#IMPLIMENTING VARIABLES
#starts logging
logger.setLevel(logging.DEBUG)
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s'))
logger.addHandler(handler)
#makes the bot able to use member privileges
intents.members = True
intents.messages = True
#establish and implement bot
bot = commands.Bot(command_prefix=commands.when_mentioned_or('!'), description=description, intents=intents)

#wrestler object
class Wrestler:
  #constructor
  def __init__(self, name):
    update_wrestler(name)
#Match Object
class Match:
  def __init__(self, *wrestlers):
    self.contestents = wrestlers
    self.pool = 0
  def increase_pool(self):
    self.pool = self.pool + 1
  def get_pool():
    return self.pool

#Global Match Variable
nextmatch : Match
#update wrestler database
def update_wrestler(name):
  if "wrestlername" in db.keys():
    names = db["wrestlername"]
    names.append(name)
    db["wrestlername"] = names
  else:
    db["wrestlername"] = [name]
  if "wrestlerwins" in db.keys():
    wins = db["wrestlerwins"]
    wins.append(0)
    db["wrestlerwins"] = wins
  else:
    db["wrestlerwins"] = [0]
  if "wrestlerloss" in db.keys():
    loss = db["wrestlerloss"]
    loss.append(0)
    db["wrestlerloss"] = loss
  else:
    db["wrestlerloss"] = [0]
#del wrestler name database
def delete_wrestlername(index):
  names = db["wrestlername"]
  wins = db["wrestlerwins"]
  loss = db["wrestlerloss"]
  if len(names) > index:
    del names[index]
    del wins[index]
    del loss[index]
    db["wrestlername"] = names
    db["wrestlerwins"] = wins
    db["wrestlerloss"] = loss
#get index of wrestler
def get_index(name):
  if "wrestlername" in db.keys():
    names = db["wrestlername"]
    if name in names:
      index = names.index(name)
      return index
#set wins
def set_wins(name, x):
  if "wrestlername" in db.keys():
    names = db["wrestlername"]
    if name in names:
      index = get_index(name)
      db["wrestlerwins"][index] = x
#set losses
def set_loss(name, x):
  if "wrestlername" in db.keys():
    names = db["wrestlername"]
    if name in names:
      index = get_index(name)
      db["wrestlerloss"][index] = x
#user object
class User:
  def __init__(self, name):
    self.name = name
#COMMANDS AND SUCH
#log start in console
@bot.event
async def on_ready():
  print('Logged on as {0.user}!'.format(bot))
#log user messages in console for troubleshooting, aswell as processing commands
@bot.event
async def on_message(message):
  print('Message from {0.author}: {0.content}'.format(message))
  await bot.process_commands(message)
#welcome message
@bot.event
async def on_member_join(member):
  guild = member.guild
  if guild.system_channel is not None:
    to_send = 'Welcome {0.mention} to {1.name}!'.format(member, guild)
  await guild.system_channel.send(to_send)
#echo command
@bot.command()
async def echo(self, message : str):
  print('echo command accepted with "{0}" parameters'.format(message))
  await self.send(message + '\nIs there an echo in here?')
#add wrestler
@bot.command()
async def wrestler(self, name):
  print('wrestler command accepted with "{0}" parameters'.format(name))
  await self.send("Wrestler {0} added".format(name))
#list current wrestlers
@bot.command()
async def list(self):
  print('list command accepted')
  print(db.keys())
  if "wrestlername" in db.keys():
    troubleshootnames= "current array of names "
    troubleshootloss = "current array of losses "
    troubleshootwins = "current array of wins "
    for x in db["wrestlername"]:
      troubleshootnames = troubleshootnames + x + ", "
    for x in db["wrestlerwins"]:
      troubleshootwins = troubleshootwins + str(x) + ", "
    for x in db["wrestlerloss"]:
      troubleshootloss = troubleshootloss + str(x) + ", "
    print(troubleshootwins)
    print(troubleshootloss)
    print(troubleshootnames)
    message = "List of current wrestlers "
    for x in range(len(db["wrestlername"])):
      message = message + db["wrestlername"][x] + "(" + str(db["wrestlerwins"][x]) + "," + str(db["wrestlerloss"][x]) + "), "
    await self.send(message) 
  else:
    await self.send(empty)
    print('Nothing in Database')
#remove wrestler
@bot.command()
async def delwrestler(self, name):
  print('del command accepted with "{0}" parameters'.format(name))
  if "wrestlername" in db.keys():
    names = db["wrestlername"]
    if name in names:
      index = get_index(name)
      delete_wrestlername(index)
      await self.send('Wrestler {0} removed from database'.format(name))
    else:
      await self.send('No wrestler with name {0} in database'.format(name))
  else:
    await self.send(empty)
#Set record
@bot.command()
async def setrecord(self, wrestler, wins, loss):
  print('setrecord command accepted with {0} wins and {1} losses'.format(wins, loss))
  if "wrestlername" in db.keys():
    names = db["wrestlername"]
    if wrestler in names:
      index = get_index(wrestler)
      set_wins(wrestler, wins)
      set_loss(wrestler, loss)
      await self.send("Wrestler {0} record adjusted to (".format(wrestler) + str(db["wrestlerwins"][index]) + "," + str(db["wrestlerloss"][index]) + ")")
    else:
      await self.send("No wrestler with name {0} found. Use !list to see a list of currently registered wrestlers.".format(wrestler))
  else:
    await self.send(empty)
#Display the recod of a specific wrestler
@bot.command()
async def record(self, wrestler):
  print('record command accepted with name {0}'.format(wrestler))
  if "wrestlername" in db.keys():
    names = db["wrestlername"]
    if wrestler in names:
      index = get_index(wrestler)
      await self.send(db["wrestlername"][index] + "(" + str(db["wrestlerwins"][index]) + "," + str(db["wrestlerloss"][index]) + ")")
    else:
      await self.send("No wrestler with name {0} found. Use !list to see a list of currently registered wrestlers.".format(wrestler))
  else:
    await self.send(empty)
#command to construct Match
@bot.command()
async def match(self, *wrestlers):
  print('match command accepted with ' + '{} arguments: {}'.format(len(wrestlers), ', '.join(wrestlers)))
  if "wrestlername" in db.keys():
    names = db["wrestlername"]
    if set(wrestlers).issubset(set(names)):
      message = "Next match is between "
      for x in wrestlers:
        index = get_index(x)
        message = message + x + " (" + str(db["wrestlerwins"][index]) + "," + str(db["wrestlerloss"][index]) + ")"
      await self.send(message)
    else:
      await self.send("One of the wrestlers you entered doesnt match the database; this is where it would tell you which one if i was a good programmer")
  else:
    await self.send("No wrestlers in database, add them with the '!wrestler' command") 
#start bot
bot.run(token)