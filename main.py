import discord
import asyncio
import random
import pickle

client = discord.Client()

def checkIfJoined(player):
    for innedPlayer in innedPlayerlist:
        if innedPlayer == player:
            return True
    return False

def isAdmin(user):
    #find if user is admin or mod. If so, return true
    await client.send_message(message.channel, 'You don\'t have permission to use that command')

def remind(reminder, whoToRemind):
    #Add people to list of people to remind
    #Message the list periodically with reminders
    
def bedtime(message):
    if isAdmin(message.author):
        #Set 'bedtime' for user based on message parsing
    
@client.event
async def on_ready():
    print(client.user.name, end="")
    print(client.user.id, end="")
    print("is up and running!")
    print('------')
    innedPlayerlist = []

@client.event
async def on_message(message):
    if message.content.startswith('!'):
        if message.content.startswith('!join'):
            if not checkIfJoined(message.author):
                innedPlayerList.append(message.author)
                await client.send_message(message.channel, 'You\'ve successfully joined the player list, ' + message.author + '. There are currently ' + str(playerList.length()) + 'players waiting for the game to start.')
            else:
                await client.send_message(message.channel, 'You\'re already on the player list!')
                
        elif message.content.startswith('!start'):
            if playerList.length() > 4:
                #Start game based on inned playerlist
            else:
                await client.send_message(message.channel, 'You need at least 5 players to start a game!')
            
        elif message.content.startswith('!remindMe'):
            #Parse out '!remindMe' (Everything after first space)
            await remind(reminder,message.author)
            await client.send_message(message.channel, 'Ok, ' + message.author + ', I\'ll remind you to ' + reminder + '.')
            
        elif message.content.startswith('!addquote')
            if not quoteList:
                with open("quoteDoc.pk1","rb") as quoteFile
                    quoteList = pickle.load(quoteFile)
            quoteList[len(quoteList)] = message.content[9:]
            
        elif message.content.startswith('!quote'):
            if not quoteList:
                with open("quoteDoc,pk1","rb") as quoteFile:
                    quoteList = pickle.load(quoteFile)
            await client.send_message(message.channel, quoteList[random.randrange(0,len(quoteList)))
            
        elif message.content.startswith('!bedtime'):
            if isAdmin(message.author):
                await bedtime(message)
              
        elif message.content.startswith('!remind '):
            if isAdmin(message.author):
                #Take first UserID as whoToRemind
                #Parse out first UserID and '!remind ' (everything after second space)
                #set modified reminder to reminder with all "your" changed to "their"
                await remind(reminder,whoToRemind)
                await client.send_message(message.channel, 'Ok, ' + message.author + ', I\'ll remind ' + whoToRemind + ' to ' + modifiedReminder)
        
