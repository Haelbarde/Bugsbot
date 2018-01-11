import discord
import asyncio
import random
import logging
import config
from gameSuperclass import *

class ResistanceInstance(GameInstance):
    #Initate all variables to their default state
    def __init__(self, gameChannel, client):
        super().__init__(gameChannel, client, "Resitance")
        self.missionCounter = 0
        self.missionSuccessCount = 0
        self.missionFailureCount = 0
        self.rejectedMissionCount = 0
        self.missionArray = {}
        self.spyList = []
        self.leader = False
        self.leaderCounter = 0

        

       


        # self.presidentCounter = 0
        # self.facistPolicies = 0
        # self.liberalPolicies = 0
        # self.SHMode = 0
        # self.skipThreshold = False
        # self.playerElected = False
        # self.voteOutcome = False
        # self.nominatedPlayer = False
        # self.newFascist = False
        # self.president = False
        # self.chancellor = False
        # self.hitler = False
        # self.enactedPolicy = False
        # self.vetoEnabled = False
        # self.unanimousVeto = False
        # self.lastChancellor = False
        # self.lastPresident = False
        # self.peekEnabled = False
        # self.voteArray = {}
        # self.skipArray = {}
        # self.turnDeck = []
        # self.fascists = []
        # self.policyDeck = ["Fascist","Fascist","Fascist","Fascist","Fascist","Fascist","Fascist","Fascist","Fascist","Fascist","Fascist",
        #                    "Liberal","Liberal","Liberal","Liberal","Liberal","Liberal"]
        # self.fullDeck = ["Fascist","Fascist","Fascist","Fascist","Fascist","Fascist","Fascist","Fascist","Fascist","Fascist","Fascist",
        #                  "Liberal","Liberal","Liberal","Liberal","Liberal","Liberal"]

    #Add facist to facist list, accounting for duplicates 
    def addSpy(self):
        self.newSpy = self.innedPlayerlist[random.randrange(0,self.playerCount)]
        if self.newSpy in self.spyList:
            self.addSpy()
        else:
            self.spyList.append(self.newSpy)

    # #Select Hitler, making sure selected user isn't actually a facist
    # def addHitler(self):
    #     self.hitler = self.innedPlayerlist[random.randrange(1,self.numOfPlayers)]
    #     if self.hitler in self.fascists:
    #         self.addHitler()

    #Invoke previous 2 functions
    def assignRoles(self):
        self.spyList = []
        for x in range(0,self.spyCount):
            self.addSpy()
        # self.addHitler()

    #Send role PMs to facists
    async def sendMessages(self):
        if self.ResistMode == 1: # 5-6 players, 2 spies
            await self.client.send_message(self.spyList[0], "You are a Spy. Your teammate is " + self.spyList[1].name)
            await self.client.send_message(self.spyList[1], "You are a Spy. Your teammate is " + self.spyList[0].name)
        elif self.ResistMode == 2: # 7-9 players, 3 spies
            await self.client.send_message(self.spyList[0], "You are a Spy. Your teammates are " + self.spyList[1].name + " and " + self.spyList[2].name)
            await self.client.send_message(self.spyList[1], "You are a Spy. Your teammates are " + self.spyList[0].name + " and " + self.spyList[2].name)
            await self.client.send_message(self.spyList[2], "You are a Spy. Your teammates are " + self.spyList[0].name + " and " + self.spyList[1].name)
        elif self.ResistMode == 3: # 10 players, 4 spies
            await self.client.send_message(self.spyList[0], "You are a Spy. Your teammates are " + self.spyList[1].name 
                                                        + ", " + self.spyList[2].name + ", and " + self.spyList[3].name)
            await self.client.send_message(self.spyList[1], "You are a Spy. Your teammates are " + self.spyList[0].name 
                                                        + ", " + self.spyList[2].name + ", and " + self.spyList[3].name)
            await self.client.send_message(self.spyList[2], "You are a Spy. Your teammates are " + self.spyList[0].name 
                                                        + ", " + self.spyList[1].name + ", and " + self.spyList[3].name)                                                                                        
            await self.client.send_message(self.spyList[3], "You are a Spy. Your teammates are " + self.spyList[0].name 
                                                        + ", " + self.spyList[1].name + ", and " + self.spyList[2].name)

        for x in self.innedPlayerlist:
            if not (x in self.spyList):
                await client.send_message(x, "You are a  proud member of the Resistance!")

    #Selects the president based on iterable integer        
    async def assignLeader(self):
        self.leader = self.innedPlayerlist[self.leaderCounter%self.playerCount]
        await self.client.send_message(self.gameChannel, ("The new Team Leader is <@{}>.\nTeam Leader, please nominate <@{}> player(s) for the current mission "
                                                          "by using `!nominate @playername`").format(self.leader.id, self.missionArray[self.missionCounter]))

# TO DO ===================================================================================================================
    #Waits for nomination
    async def nomination(self):
        if self.over:
            return True
        playerNominated = False
        warningGiven = False
        while not playerNominated:
            nominationMessage = await self.client.wait_for_message(author=self.president, channel = self.gameChannel)
            try:
                self.nominatedPlayer = nominationMessage.mentions[0]
                if self.nominatedPlayer in self.innedPlayerlist:

                    if (self.nominatedPlayer != self.lastChancellor) and (self.nominatedPlayer != self.lastPresident):
                        playerNominated = True
                        await self.client.send_message(self.gameChannel, ("President {} has nominated {} for Chancellor. Please preface your vote with an '!'. Most "
                                                                          "forms of 'yes' or 'no' are supported.").format(self.president.name,
                                                                                                                          self.nominatedPlayer.name))
                    else:
                        self.nominatedPlayer = False
                        await self.client.send_message(self.gameChannel, "I'm sorry, but your nominee was term limited! Please nominate someone else.")
                else:
                    self.nominatedPlayer = False
                    await self.client.send_message(self.gameChannel, "You didn't enter a valid nomination message!")
            except IndexError:
                if not warningGiven:
                    await self.client.send_message(self.gameChannel, "Please mention the person you're nominating like this: `@user`")
                    warningGiven = True

    #Collect votes from users
    async def vote(self):
        if self.over:
            return True
        self.voteArray = {}
        votesCast = 0
        for player in self.innedPlayerlist:
            self.voteArray[player] = "Uncast"
        while not votesCast==self.numOfPlayers or self.skipThreshold:
            votingMessage = await self.client.wait_for_message()
            messageStart = (votingMessage.content.split(" "))[0].lower()

            #if skipping
            if (votingMessage.author in self.innedPlayerlist) and messageStart == "!skip":
                if self.skipArray == {}:
                    await client.send_message(self.gameChannel, ("{} has begun a vote to end the election early. This requires a majority of the current players to"
                                                                " pass. Please say `!skip` if you'd like to be counted.").format(message.author))
                    self.skipArray[message.author] = True
                else:
                    self.skipArray[message.author] = True
                    await client.send_message(self.gameChannel, "{} has requested to skip".format(votingMessage.author))
                    if len(self.skipArray) > self.numOfPlayers/2:
                        self.skipThreshold = True

            #if voting yes
            if (votingMessage.author in self.innedPlayerlist) and messageStart in config.affirmatives:
                if self.voteArray[votingMessage.author] == "Uncast":
                    votesCast = votesCast + 1
                    await self.client.send_message(self.gameChannel, "{} has cast a vote".format(votingMessage.author.name))
                elif self.voteArray[votingMessage.author] == "No":
                    await self.client.send_message(self.gameChannel, "{} has changed their vote".format(votingMessage.author.name))
                else:
                    await self.client.send_message(self.gameChannel, "You're already voting yes, {}".format(votingMessage.author.name))
                self.voteArray[votingMessage.author] = "Yes"

            #if voting no
            elif(votingMessage.author in self.innedPlayerlist) and messageStart in config.negatives:
                if self.voteArray[votingMessage.author] == "Uncast":
                    votesCast = votesCast + 1
                    await self.client.send_message(self.gameChannel, "{} has cast a vote".format(votingMessage.author.name))
                elif self.voteArray[votingMessage.author] == "Yes":
                    await self.client.send_message(self.gameChannel, "{} has changed their vote".format(votingMessage.author.name))
                else:
                    await self.client.send_message(self.gameChannel, "You're already voting no, {}".format(votingMessage.author.name))
                self.voteArray[votingMessage.author] = "No"
        self.skipArray = {}
        self.skipThreshold = False

    #Counts user votes, sets self.voteOutcome to bool depending on outcome
    async def countVote(self):
        yesVotes = 0
        noVotes = 0
        for player in self.innedPlayerlist:
            if self.voteArray[player] == "Yes":
                yesVotes = yesVotes + 1
            elif self.voteArray[player] == "No":
                noVotes = noVotes + 1
        messageString = ""
        for x in self.voteArray:
            messageString = messageString + "{} voted {}\n".format(x.name, self.voteArray[x])
        await self.client.send_message(self.gameChannel, messageString)
        if yesVotes > noVotes:
            self.voteOutcome = True
        else:
            self.voteOutcome = False

    # async def genPolicies(self):
    #     self.turnDeck = []
    #     print(len(self.policyDeck))
    #     #If there are more than 3 policies, select from the deck at random
    #     if len(self.policyDeck) > 3:
    #         i = 0
    #         print("More than 3")
    #         while i < 3:
    #             chosenPolicy = random.randrange(0,len(self.policyDeck))
    #             self.turnDeck.append(self.policyDeck.pop(chosenPolicy))
    #             i = i + 1

    #     #If there are 3 policies, use the entire deck
    #     elif len(self.policyDeck) == 3:
    #         print("3")
    #         self.turnDeck = list(self.policyDeck)
    #         self.policyDeck = self.fullDeck

    #     #If there are fewer than 3 policies, shuffle in discards and try drawing again
    #     else:
    #         print("Fewer than 3")
    #         self.policyDeck = self.fullDeck
    #         await self.genPolicies()
    #         print("Tail recursion finished")

    #     #Show president top 3 if peek enabled
    #     if self.peekEnabled:
    #         self.peekEnabled = False
    #         await self.client.send_message(self.president, ("You peeked at the following 3 policies:\n"
    #                                                         "1: {}\n2: {}\n3: {}\n").format(self.turnDeck[0],self.turnDeck[1],self.turnDeck[2]))

    async def missionPhase(self):
        for player in self.missionPlayerList:
            await self.client.send_message(self.player, "You are on the current mission.")
            if player in self.spyList:
                await self.client.send_message(self.player, "1: Succeed this mission\n2: Fail this mission")
                if (self.specialForthMission && self.missionCounter == 4):
                    await self.client.send_message(self.player, "Note that 2 failures are required to fail this mission.")
            elif:
                 await self.client.send_message(self.player, "1: Succeed this mission")
            # NEED TO MAKE SURE THAT IT LISTENS TO MULTIPLE PLAYERS AT THE SAME TIME.

    async def presPolicies(self):
        await self.client.send_message(self.president, ("You drew the following 3 policies:\n1: {}\n2: {}\n3: {}\nPlease select a policy to discard by saying "
                                                        "the number of the policy you'd like to remove").format(self.turnDeck[0],self.turnDeck[1],self.turnDeck[2]))
        def check(reply):
            if self.over:
                return True
            bool1 = (reply.content[0] == "1" or reply.content[0] == "2" or reply.content[0] == "3")
            bool2 = reply.channel.is_private and reply.author==self.president
            return (bool1 and bool2)
        reply = await self.client.wait_for_message(check=check)
        if self.over:
            return True
        await self.client.send_message(self.president, "You've passed the other 2 cards to the chancellor.")     
        if reply.content[0] == "1":
            self.turnDeck.pop(0)
        elif reply.content[0] == "2":
            self.turnDeck.pop(1)
        else:
            self.turnDeck.pop(2)

    async def chancellorPolicies(self):
        await self.client.send_message(self.chancellor, ("You were passed the following 2 policies:\n1: {}\n2: {}\nPlease choose a policy to enact by saying "
                                                         "the number of the policy you'd like to select").format(self.turnDeck[0],self.turnDeck[1]))
        def check(reply):
            if self.over:
                return True
            bool1 = (reply.content[0] == "1" or reply.content[0] == "2" or (reply.content=="!veto" and self.vetoEnabled == True))
            bool2 = reply.channel.is_private and reply.author==self.chancellor
            return (bool1 and bool2)
        reply = await self.client.wait_for_message(check=check)
        print("Proper reply found")
        if self.over:
            return True
        if reply.content[0] == "1":
            self.enactedPolicy = self.turnDeck[0]
            await self.client.send_message(self.chancellor, "You've enacted a {} policy".format(self.enactedPolicy))
        elif reply.content[0] == "2":
            self.enactedPolicy = self.turnDeck[1]
            await self.client.send_message(self.chancellor, "You've enacted a {} policy".format(self.enactedPolicy))
        else:
            await self.client.send_message(self.gameChannel, "The Chancellor has chosen to veto the agenda. <@{}>, do you agree?".format(self.president.id))
            properReply = False
            while not properReply:
                reply = await self.client.wait_for_message(author=self.president)
                if reply in config.affirmatives:
                    self.unanimousVeto = True
                    properReply = True
                elif reply in config.negatives:
                    self.unanimousVeto = False
                    properReply = True
                else:
                    await self.client.send_message(self.gameChannel, "That wasn't a recognized answer. Try again, please")

    async def presInvestigate(self):
        messageToPres = "Who would you like to investigate? Your choices are:\n"
        for x in range(len(self.innedPlayerlist)):
            nextPlayer = "{}: {}\n".format(x+1, self.innedPlayerlist[x])
            messageToPres = messageToPres + nextPlayer
        await self.client.send_message(self.president, messageToPres + "Please respond with a number between 1 and {}".format(x+1))
        properResponse = False
        bool1 = True
        while not (bool1 and properResponse):
            reply = await self.client.wait_for_message()
            if self.over:
                return True
            if not reply.author==self.president:
                bool1 = False
            else:
                print("Response Recorded - Investigate")
            if not reply.channel.is_private:
                bool1 = False
            else:
                print("Channel Recognized as private - Investigate")
            if bool1:
                try:
                    int(reply.content[0])
                    print("Int recognized - Investigate")
                    for y in range(len(self.innedPlayerlist)):
                        if y == int(reply.content[0]) - 1:
                            print("y is in range - Investigate")
                            if not self.president == self.innedPlayerlist(y):
                                properResponse = True
                                print("Response deemed proper - investigate")
                            else:
                                await self.client.send_message(self.president, "I'm pretty sure you don't want to investigate yourself. Let's try that again")
                                bool1 = False
                    if not (properResponse):
                        if bool1:
                            await self.client.send_message(self.president, "The number you entered was out of range")
                            bool1 = False
                except TypeError:
                    print("Didn't recognize int - Investigate")
                    self.client.send_message(self.president, "That was not a valid integer! Try again")
                    bool1 = False
        print("Loop Escaped - Investigate")
        if (self.innedPlayerlist[int(reply.content[0]) - 1]) in self.fascists or (self.innedPlayerlist[int(reply.content[0]) - 1] == self.hitler):
            self.client.send_message(self.president, "{} is a member of the Fascist party!".format(self.innedPlayerlist[int(reply.content[0]) - 1].name))
        else:
            self.client.send_message(self.president, "{} is a member of the Liberal party.".format(self.innedPlayerlist[int(reply.content[0]) - 1].name))

    async def presKill(self):
        messageToPres = "Who would you like to kill? Your choices are:\n"
        for x in range(len(self.innedPlayerlist)):
            nextPlayer = "{}: {}\n".format(x+1, self.innedPlayerlist[x])
            messageToPres = messageToPres + nextPlayer
        await self.client.send_message(self.president, messageToPres + "Please respond with a number between 1 and {}".format(x+1))
        print("Message sent - Kill")
        properResponse = False
        bool1 = True
        while not (properResponse and bool1):
            reply = await self.client.wait_for_message()
            if self.over:
                return True
            if reply.author==self.president:
                print("Message received - Kill")
                bool1 = True
            else:
                bool1 = False
            try:
                int(reply.content[0])
                print("Message recognized as int - Kill")
                for y in range(len(self.innedPlayerlist)):
                    if y == int(reply.content[0]) - 1:
                        print("Target identified - Kill")
                        if not self.president == self.innedPlayerlist(y):
                            print("Proper Response - Kill")
                            properResponse = True
                        else:
                            print("Self-Targeting - Kill")
                            await self.client.send_message(self.president, ("I'm pretty sure you don't want to kill yourself. Let's try that again.\nIf you are "
                                                                            "feeling suicidal, please call the suicide prevention hotline at 1-800-273-8255"))
                print("Out of range - Kill")
                await self.client.send_message(self.president, "The number you entered was out of the range")
            except TypeError:
                print("Response not valid - Kill")
                self.client.send_message(self.president, "That was not a valid integer! Try again")
        killedPlayer = self.innedPlayerlist.pop(int(reply.content[0]) - 1)
        self.numOfPlayers = self.numOfPlayers - 1
        self.client.send_message(self.gameChannel, "{} has been killed!".format(killedPlayer.name))
        self.over = self.checkIfWon()

    async def addPolicy(self, policy):
        if policy == "Fascist":
            self.facistPolicies = self.facistPolicies + 1
            if self.SHMode == 1: #numOfPlayers < 7
                if self.facistPolicies == 3:
                    self.peekEnabled = True
                elif self.facistPolicies == 4:
                    await self.presKill()
                elif self.facistPolicies == 5:
                    await self.presKill()
                    self.vetoEnabled = True
            elif self.SHMode == 2:
                if self.facistPolicies == 2:
                    await self.presInvestigate()
                elif self.facistPolicies == 3:
                    #await self.specialElection()
                    pass
                elif self.facistPolicies == 4:
                    await self.presKill()
                elif self.facistPolicies == 5:
                    await self.presKill()
                    self.vetoEnabled = True
            elif self.SHMode == 3:
                if self.facistPolicies in [1,2]:
                    await self.presInvestigate()
                elif self.facistPolicies == 3:
                    #await self.specialElection()
                    pass
                elif self.facistPolicies == 4:
                    await self.presKill()
                elif self.facistPolicies == 5:
                    await self.presKill()
                    self.vetoEnabled = True
        elif policy == "Liberal":
            self.liberalPolicies = self.liberalPolicies + 1        

    async def checkIfWon(self):
        # onlyFascists = True
        # for innedPlayer in self.innedPlayerlist:
        #     if not innedPlayer in self.fascists:
        #         onlyFascists = False
        if (self.missionSuccessCount == 3)
            await self.client.send_message(self.gameChannel, "The Resistance succesfully completed three missions! They win!")
        elif (self.missionFailureCount == 3)
            await self.client.send_message(self.gameChannel, "The Spys succesfully caused three missions to fail! They win!")
        elif (self.rejectedMissionCount == 5)
            await self.client.send_message(self.gameChannel, "Five proposed teams have been rejected, and the Resistance is in disarray... The Spies win!")
        else:
            return False
        return True

    async def trollAonar(self):
        for x in self.innedPlayerlist:
            if x.id == "263436294020005888" or x.id == 263436294020005888:
                await self.client.send_message(x, "Use the following link to see your role: <https://goo.gl/9iFFHz>")


async def votePasses(game):
    game.chancellor = game.nominatedPlayer
    game.nominatedPlayer = False
    game.over = await game.checkIfWon()
    if not game.over:
        await game.client.send_message(game.gameChannel, ("The vote succeeded! President {} and Chancellor {} "
                                                          "are now choosing policies.").format(game.president.name, game.chancellor.name))
        game.lastChancellor = False
        game.lastPresident = False
        await game.presPolicies()
        if game.over:
            return True
        await game.chancellorPolicies()
        if not game.unanimousVeto:
            game.playerElected = True
        else:
            await game.genPolicies()
            failedElections = failedElections + 1

async def threeFailures(game):
    topPolicy = game.turnDeck.pop(0)
    game.policyDeck.append(game.turnDeck[0])
    game.policyDeck.append(game.turnDeck[1])
    await game.addPolicy(topPolicy)
    await game.client.send_message(game.gameChannel, "Because 3 governments failed, a {} policy was enacted at random".format(topPolicy))
    failedElections = 0
    await game.genPolicies()
    game.presidentCounter = game.presidentCounter+1
    game.over = await game.checkIfWon()

async def startGame(message):
    game = config.gameInstances[message.channel.id]
    await game.trollAonar()
    game.playerCount = len(game.innedPlayerlist)
    if game.playerCount == 5:
        game.missionArray = [2, 3, 2, 3, 3]
        game.specialForthMission = False
        game.spyCount = 2
        
    if game.playerCount == 6:
        game.missionArray = [2, 3, 4, 3, 4]
        game.specialForthMission = False
        game.spyCount = 2
    if game.playerCount == 7:
        game.missionArray = [2, 3, 3, 4, 4]
        game.specialForthMission = True
        game.spyCount = 3
    if game.playerCount > 7:
        game.missionArray = [3, 4, 4, 5, 5]
        game.specialForthMission = True
        if game.playerCount == 10:
            game.spyCount = 4
        elif:
            game.spyCount = 3
    game.assignRoles()
    await game.sendMessages()
    game.leaderCounter = random.randrange(0,game.playerCount)
    await mainGame(game)

async def mainGame(game):
    while not game.over:
        #create game.turnDeck
        await game.genPolicies()

        #Start nomination cycle
        failedElections = 0
        game.playerElected = False
        while not game.playerElected:
            await game.assignPres() #Choose president based on iterated value 
            await game.nomination() #Nominate president
            await game.vote()       #Get players' votes
            await game.countVote()  #Count votes, game.voteOutcome is the result

            #Escape if game has ended 
            if game.over:
                break

            #Go through all policy selections
            if game.voteOutcome:
                await votePasses(game)

            #Switch to next president, repeat
            elif failedElections<2:
                failedElections = failedElections + 1
                game.presidentCounter = game.presidentCounter + 1 #Iterate to next president

            #Draw from top, reset failedElections counter, iterate to next president
            else:
                await threeFailures(game)

        #Escape if game has ended      
        if game.over:
            break

        #Enact policies
        print("Enacting Policy")
        await game.addPolicy(game.enactedPolicy)
        print("Policy Enacted")
        await game.client.send_message(game.gameChannel, ("President {} and Chancellor {} have enacted a {} policy.\nThere are now {} fascist policies"
                                                          " and {} liberal policies in play.").format(game.president.name, game.chancellor.name, game.enactedPolicy,
                                                                                                      game.facistPolicies, game.liberalPolicies))
        #Set term limits and update roles
        game.lastChancellor = game.chancellor
        game.lastPresident = game.president
        game.chancellor = False

        #Check if enacted policy caused victory
        game.over = await game.checkIfWon()

        #Iterate to next president 
        game.presidentCounter += 1

    #Reset game once over
    print("Game over")
    config.gameInstances[game.gameChannel.id] = SHInstance(game.gameChannel, game.client)
    
