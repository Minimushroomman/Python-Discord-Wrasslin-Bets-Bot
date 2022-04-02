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
empty = "No wrestlers found in database, use '!wrestler' to add one"

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

#FUNCTIONS
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

#return wintger
def get_wins(name):
  if "wrestlername" in db.keys():
    names = db["wrestlername"]
    if name in names:
      index = get_index(name)
      return db["wrestlerwins"][index]

#set losses
def set_loss(name, x):
  if "wrestlername" in db.keys():
    names = db["wrestlername"]
    if name in names:
      index = get_index(name)
      db["wrestlerloss"][index] = x

#return loss
def get_loss(name):
  if "wrestlername" in db.keys():
    names = db["wrestlername"]
    if name in names:
      index = get_index(name)
      return db["wrestlerloss"][index]

#add users
def update_users(name):
  if "users" in db.keys():
    names = db["users"]
    names.append(name)
    db["users"] = names
  else:
    db["users"] = [name]
  if "bank" in db.keys():
    values = db["bank"]
    values.append(0)
    db["bank"] = values
  else:
    db["bank"] = [0]

#return user index
def get_user_index(name):
  if "users" in db.keys():
    names = db["users"]
    if name in names:
      index = names.index(name)
      return index

#set a users bank
def set_bank(user, x):
  if "users" in db.keys():
    names = db["users"]
    if user in names:
      index = get_user_index(user)
      db["bank"][index] = x

#return contender index
def get_contender_index(name):
  if "contenders" in db.keys():
    contenders = db["contenders"]
    if name in contenders:
      index = contenders.index(name)
      return index

#get total of current pool
def get_pool():
  if "pool" in db.keys():
    p = db["pool"]
    total = 0
    for x in p:
      total = total + x
    return total

#wipe match parameters
def wipe():
  if "contenders" in db.keys():
    c = db["contenders"]
    c.clear()
    db["contenders"] = c
  if "pool" in db.keys():
    p = db["pool"]
    p.clear()
    db["pool"] = p
  if "contender0" in db.keys():
    c0 = db["contender0"]
    c0.clear()
    db["contender0"] = c0
  if "contender1" in db.keys():
    c1 = db["contender1"]
    c1.clear()
    db["contender1"] = c1
  if "contender2" in db.keys():
    c2 = db["contender2"]
    c2.clear()
    db["contender2"] = c2
  if "contender3" in db.keys():
    c3 = db["contender3"]
    c3.clear()
    db["contender3"] = c3
  if "contender4" in db.keys():
    c4 = db["contender4"]
    c4.clear()
    db["contender1"] = c4
  if "contender5" in db.keys():
    c5 = db["contender5"]
    c5.clear()
    db["contender5"] = c5
  if "contender6" in db.keys():
    c6 = db["contender5"]
    c6.clear()
    db["contender6"] = c6
  if "contender7" in db.keys():
    c7 = db["contender5"]
    c7.clear()
    db["contender7"] = c7

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
  update_wrestler(name)
  await self.send("Wrestler {0} added".format(name))

#list current wrestlers
@bot.command()
async def list(self):
  print('list command accepted')
  print(db.keys())
  troubleshootnames= "current array of names  "
  troubleshootloss = "current array of losses "
  troubleshootwins = "current array of wins   "
  troubleshootusers ="current array of users  "
  troubleshootbank = "current array of bank   "
  troubleshootcontenders = "current array of contenders "
  troubleshootpool =       "current array of pool       "
  troubleshootcontender0 = "current users betting on 0 "
  troubleshootcontender1 = "current users betting on 1 "
  troubleshootcontender2 = "current users betting on 2 "
  troubleshootcontender3 = "current users betting on 3 "
  troubleshootcontender4 = "current users betting on 4 "
  troubleshootcontender5 = "current users betting on 5 "
  troubleshootcontender6 = "current users betting on 6 "
  troubleshootcontender7 = "current users betting on 7 "
  if "wrestlername" in db.keys():
    for x in db["wrestlername"]:
      troubleshootnames = troubleshootnames + x + ", "
  else:
    troubleshootnames = "no database of wrestlers"
  if "wrestlerwins" in db.keys():
    for x in db["wrestlerwins"]:
      troubleshootwins = troubleshootwins + str(x) + ", "
  else:
    troubleshootwins = "no database of wins"
  if "wrestlerloss" in db.keys():
    for x in db["wrestlerloss"]:
      troubleshootloss = troubleshootloss + str(x) + ", "
  else:
    troubleshootloss = "no database of losses"
  if "users" in db.keys():
    for x in db["users"]:
      troubleshootusers = troubleshootusers + x + ", "
  else:
    troubleshootusers = "no database of users"
  if "bank" in db.keys():
    for x in db["bank"]:
      troubleshootbank = troubleshootbank + str(x) + ", "
  else:
    troubleshootbank = "no database of bank"
  if "contenders" in db.keys():
    for x in db["contenders"]:
      troubleshootcontenders =  troubleshootcontenders + x + ", "
  else:
    troubleshootcontenders = "no database of contenders"
  if "pool" in db.keys():
    for x in db["pool"]:
      troubleshootpool = troubleshootpool + str(x) + ", "
  else:
    troubleshootpool = "no database for pool"
  if "contender0" in db.keys():
    for x in db["contender0"]:
      troubleshootcontender0 = troubleshootcontender0 + x + ", "
  else:
    troubleshootcontender0 = "no database for contender0"
  if "contender1" in db.keys():
    for x in db["contender1"]:
      troubleshootcontender1 = troubleshootcontender1 + x + ", "
  else:
    troubleshootcontender1 = "no database for contender1"
  if "contender2" in db.keys():
    for x in db["contender2"]:
      troubleshootcontender2 = troubleshootcontender0 + x + ", "
  else:
    troubleshootcontender2 = "no database for contender2"
  if "contender3" in db.keys():
    for x in db["contender3"]:
      troubleshootcontender3 = troubleshootcontender3 + x + ", "
  else:
    troubleshootcontender3 = "no database for contender3"
  if "contender4" in db.keys():
    for x in db["contender4"]:
      troubleshootcontender4 = troubleshootcontender4 + x + ", "
  else:
    troubleshootcontender4 = "no database for contender4"
  if "contender5" in db.keys():
    for x in db["contender5"]:
      troubleshootcontender5 = troubleshootcontender5 + x + ", "
  else:
    troubleshootcontender5 = "no database for contender5"
  if "contender6" in db.keys():
    for x in db["contender6"]:
      troubleshootcontender6 = troubleshootcontender6 + x + ", "
  else:
    troubleshootcontender6 = "no database for contender6"
  if "contender7" in db.keys():
    for x in db["contender7"]:
      troubleshootcontender7 = troubleshootcontender7 + x + ", "
  else:
    troubleshootcontender7 = "no database for contender7"
  print(troubleshootnames)
  print(troubleshootwins)
  print(troubleshootloss)
  print(troubleshootusers)
  print(troubleshootbank)
  print(troubleshootcontenders)
  print(troubleshootpool)
  print(troubleshootcontender0)
  print(troubleshootcontender1)
  print(troubleshootcontender2)
  print(troubleshootcontender3)
  print(troubleshootcontender4)
  print(troubleshootcontender5)
  print(troubleshootcontender6)
  print(troubleshootcontender7)
  message = "List of current wrestlers "
  if "wrestlername" in db.keys():
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
      db["contenders"] = wrestlers
      pool = []
      for x in wrestlers:
        index = get_index(x)
        pool.append(0)
        message = message + x + " (" + str(db["wrestlerwins"][index]) + "," + str(db["wrestlerloss"][index]) + ") "
      db["pool"] = pool
      await self.send(message)
    else:
      await self.send("One of the wrestlers you entered doesnt match the database; this is where it would tell you which one if i was a good programmer")
  else:
    await self.send(empty) 

#set the winner of current match
@bot.command()
async def win(self, winner):
  print('win command accepted with name {0}'.format(winner))
  if "contenders" in db.keys():
    cont = db["contenders"]
    totpool = get_pool()
    if winner in cont:
      w = get_wins(winner)
      w = int(w) + 1
      set_wins(winner, w)
      index = get_index(winner)
      message = winner + " wins! Record updated to (" + str(db["wrestlerwins"][index]) + "," + str(db["wrestlerloss"][index]) + ") "
      cindex = get_contender_index(winner)
      if cindex == 0:
        users = db["contender0"]
      if cindex == 1:
        users = db["contender1"]
      if cindex == 2:
        users = db["contender2"]
      if cindex == 3:
        users = db["contender3"]
      if cindex == 4:
        users = db["contender4"]
      if cindex == 5:
        users = db["contender5"]
      if cindex == 6:
        users = db["contender6"]
      if cindex == 7:
        users = db["contender7"]
      winnings = totpool / len(users)
      for x in users:
        index = get_user_index(x)
        bal = db["bank"][index]
        bal = bal + winnings
        db["bank"][index] = bal
      cont.remove(winner)
      for x in cont:
        if x in db["wrestlername"]:
          l = get_loss(x)
          l = int(l) + 1
          set_loss(x, l)
          index = get_index(x)
          message = message + x + " lost! Record updated to (" + str(db["wrestlerwins"][index]) + "," + str(db["wrestlerloss"][index]) + ") "
      await self.send(message)
      wipe()
    else:
      await self.send(winner + " not in current match")
  else:
    await self.send("No current match started")

#clear match
@bot.command()
async def clearmatch(self):
  print('clearmatch command accepted')
  await self.send("Matches wiped")
  wipe()

#join betting pool
@bot.command()
async def join(self):
  name = str(self.author)
  print('join command accepted with name {0}'.format(name))
  if "users" in db.keys():
    names = db["users"]
    if name in names:
      await self.send("You have already joined the pool")
    else:
      update_users(name)
      await self.send("{0} has put their soul on the line!".format(name))
  else:
    update_users(name)
    await self.send("{0} has put their soul on the line!".format(name))

#set users bank
@bot.command()
async def setbank(self, user, x):
  print('setbank command accepted with name {0} and ammount {1}'.format(user, x))
  if "users" in db.keys():
    names = db["users"]
    if user in names:
      index = get_user_index(user)
      set_bank(user, x)
      await self.send("User {0}'s bank set to ".format(user) + str(db["bank"][index]))
    else:
      await self.send("User {0} doesn't exist in user database".format(user))
  else:
    await self.send("No user database. Have them '!join'")

#tell a users balance
@bot.command()
async def bal(self):
  print('bal command accepted from {0}'.format(str(self.author)))
  if "users" in db.keys():
    names = db["users"]
    name = str(self.author)
    if name in names:
      index = get_user_index(name)
      await self.send("{0}'s current balance: {1}".format(name, str(db["bank"][index])))
    else:
      await self.send("{0} isn't registered. Use '!join'")
  else:
    await self.send("No users have joined yet. Use '!join'")

#bet on a current match
@bot.command()
async def bet(self, contender):
  user = str(self.author)
  emessage = "{0} already bet in this match".format(user)
  print("Bet command accepted from {0} with {1} variable".format(user, contender))
  if user in db["contender0"]:
    await self.send(emessage)
  elif user in db["contender1"]:
    await self.send(emessage)
  elif user in db["contender2"]:
    await self.send(emessage)
  elif user in db["contender3"]:
    await self.send(emessage)
  elif user in db["contender4"]:
    await self.send(emessage)
  elif user in db["contender5"]:
    await self.send(emessage)
  elif user in db["contender6"]:
    await self.send(emessage)
  elif user in db["contender7"]:
    await self.send(emessage)
  else:
    if "contenders" in db.keys():
      contenders = db["contenders"]
      if contender in contenders:
        index = get_contender_index(contender)
        b = get_user_index(user)
        bank = db["bank"][b]
        bank = float(bank) - 1
        set_bank(user, bank)
        if index == 0:
          db["pool"][index] = db["pool"][index] + 1
          if "contender0" in db.keys():
            c0 = db["contender0"]
            c0.append(user)
            db["contender0"] = c0
          else:
            db["contender0"] = [user]
        if index == 1:
          db["pool"][index] = db["pool"][index] + 1
          if "contender1" in db.keys():
            c1 = db["contender1"]
            c1.append(user)
            db["contender1"] = c1
          else:
            db["contender1"] = [user]
        if index == 2:
          db["pool"][index] = db["pool"][index] + 1
          if "contender2" in db.keys():
            c2 = db["contender2"]
            c2.append(user)
            db["contender2"] = c2
          else:
            db["contender2"] = [user]
        if index == 3:
          db["pool"][index] = db["pool"][index] + 1
          if "contender3" in db.keys():
            c3 = db["contender3"]
            c3.append(user)
            db["contender3"] = c3
          else:
            db["contender3"] = [user]
        if index == 4:
          db["pool"][index] = db["pool"][index] + 1
          if "contender4" in db.keys():
            c4 = db["contender4"]
            c4.append(user)
            db["contender4"] = c4
          else:
            db["contender4"] = [user]
        if index == 5:
          db["pool"][index] = db["pool"][index] + 1
          if "contender5" in db.keys():
            c5 = db["contender5"]
            c5.append(user)
            db["contender5"] = c5
          else:
            db["contender5"] = [user]
        if index == 6:
          db["pool"][index] = db["pool"][index] + 1
          if "contender6" in db.keys():
            c6 = db["contender6"]
            c6.append(user)
            db["contender6"] = c6
          else:
            db["contender6"] = [user]
        if index == 7:
          db["pool"][index] = db["pool"][index] + 1
          if "contender7" in db.keys():
            c7 = db["contender7"]
            c7.append(user)
            db["contender7"] = c7
          else:
            db["contender7"] = [user]
        await self.send("{0} bets on {1}".format(user, contender))
      else:
        await self.send("{0} isn't in current match".format(contender))
    else:
      await self.send("No current match started")

#see whos betting on who
@bot.command()
async def pool(self):
  message = "Current betting pool:\n"
  if "contenders" in db.keys():
    contenders = db["contenders"]
    pool = db["pool"]
    lendex = len(contenders)
    for x in range(lendex):
      if x == 0:
        if "contender0" in db.keys():
          bet0 = db["contender0"]
          better0 = " "
          for y in bet0:
            better0 = better0 + y + ", "
          message = message + contenders[x] + "'s current pool is " + str(pool[x]) + " with" + better0 + "betting on them.\n"
      if x == 1:
        if "contender1" in db.keys():
          bet1 = db["contender1"]
          better1 = " "
          for y in bet1:
            better1 = better1 + y + ", "
          message = message + contenders[x] + "'s current pool is " + str(pool[x]) + " with" + better1 + "betting on them.\n"
      if x == 2:
        if "contender2" in db.keys():
          bet2 = db["contender2"]
          better2 = " "
          for y in bet2:
            better2 = better2 + y + ", "
          message = message + contenders[x] + "'s current pool is " + str(pool[x]) + " with" + better2 + "betting on them.\n"
      if x == 3:
        if "contender3" in db.keys():
          bet3 = db["contender3"]
          better3 = " "
          for y in bet3:
            better3 = better3 + y + ", "
          message = message + contenders[x] + "'s current pool is " + str(pool[x]) + " with" + better3 + "betting on them.\n"
      if x == 4:
        if "contender4" in db.keys():
          bet4 = db["contender4"]
          better4 = " "
          for y in bet4:
            better4 = better4 + y + ", "
          message = message + contenders[x] + "'s current pool is " + str(pool[x]) + " with" + better4 + "betting on them.\n"
      if x == 5:
        if "contender5" in db.keys():
          bet5 = db["contender5"]
          better5 = " "
          for y in bet5:
            better5 = better5 + y + ", "
          message = message + contenders[x] + "'s current pool is " + str(pool[x]) + " with" + better5 + "betting on them.\n"
      if x == 6:
        if "contender6" in db.keys():
          bet6 = db["contender6"]
          better6 = " "
          for y in bet6:
            better6 = better6 + y + ", "
          message = message + contenders[x] + "'s current pool is " + str(pool[x]) + " with" + better6 + "betting on them.\n"
      if x == 7:
        if "contender7" in db.keys():
          bet7 = db["contender7"]
          better7 = " "
          for y in bet7:
            better7 = better7 + y + ", "
          message = message + contenders[x] + "'s current pool is " + str(pool[x]) + " with" + better7 + "betting on them.\n"
    await self.send(message)

@bot.command()
async def balall(self):
  message = "Current Balacne for current users: "
  if "users" in db.keys():
    users = db["users"]
    for x in users:
      index = get_user_index(x)
      message = message + x + ": " + str(db["bank"][index]) + " "
    await self.send(message)
#CONNECT TO DISCORD API
#start bot
bot.run(token)