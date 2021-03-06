import asyncio
import discord
from discord.ext import commands

from watson_developer_cloud import PersonalityInsightsV3
import json
import os
import time

import utils

textChatIDlist = ["170682390786605057", "302137557896921089", "302965414793707522", "293186321395220481"] #general, dev, nsf, other

with open("secrets.txt", "r") as secretFile:
    secretKey = [key[:-1] for key in secretFile.readlines()]
    
personality_insights = PersonalityInsightsV3(
    username=secretKey[12],
    password=secretKey[13],
    version='2017-10-13')
personality_insights.set_default_headers({'x-watson-learning-opt-out': "true"})
    
def prettyMessage(filename):
    with open("Personalities/" + filename + ".txt", 'r') as file:
        profileData = json.load(file)
        
    wordCount = str(profileData["word_count"])
    
    big5 = profileData["personality"]
    needs = profileData["needs"]
    consumption = profileData["consumption_preferences"]
    values = profileData["values"]
    
    big5Result = []
    for data in range(0, len(big5)):
        big5Result.append(["__" + big5[data]["name"] + "__", str(big5[data]["percentile"] * 100)[:4] + "%"])
        for trait in range(0, len(big5[data]["children"])):
            big5Result.append([big5[data]["children"][trait]["name"], str(big5[data]["children"][trait]["percentile"] * 100)[:4] + "%"])
            
    needsResult = []
    needsResult.append(["__Needs__", ""])
    for need in range(0, len(needs)):
        needsResult.append([needs[need]["name"], str(needs[need]["percentile"] * 100)[:4] + "%"])
        
    consumptionResult = []
    for area in range(0, len(consumption)):
        consumptionResult.append(["__" + consumption[area]["name"] + "__", ""])
        for preference in range (0, len(consumption[area]["consumption_preferences"])):
            if str(consumption[area]["consumption_preferences"][preference]["score"]) == "1.0":
                consumeScore = "Likely"
            elif str(consumption[area]["consumption_preferences"][preference]["score"]) == "0.5":
                consumeScore = "Neutral"
            else:
                consumeScore = "Unlikely"
            consumptionResult.append([consumption[area]["consumption_preferences"][preference]["name"], consumeScore])
    
    valueResult = []
    valueResult.append(["__Values__", ""])
    for value in range(0, len(values)):
        valueResult.append([values[value]["name"], str(values[value]["percentile"] * 100)[:4] + "%"])
    
    totalList = []
    finalList = [big5Result, needsResult, consumptionResult, valueResult]
    for list in finalList:
        totalList.extend(list)
    #print(totalList)

    finalMessage = ""
    finalMessage += "__Personality Analysis Results__\n"
    finalMessage += ("Word Count: " + wordCount + "\n")
    for pair in totalList:
        part = pair[0] + "       " + pair[1] + "\n"
        finalMessage += (part)
    
    return finalMessage
    
def getPersonalityJSON(filename):
    if os.path.exists("Personalities/" + filename + ".txt"):
        if (os.path.getmtime("Personalities/" + filename + ".txt") < time.time() - 86400): #if a person db is more than 1 day old
            with open("MessageLogs/" + filename + ".txt") as proFile:
                profile = personality_insights.profile(
                    proFile.read(), content_type='text/plain',
                    raw_scores=True, consumption_preferences=True)
                proFile.close()
            with open("Personalities/" + filename + ".txt", 'w+') as file:
                file.write(json.dumps(profile, indent=2))

    else: #file doesn't exist, create
        with open("MessageLogs/" + filename + ".txt") as proFile:
            profile = personality_insights.profile(
                proFile.read(), content_type='text/plain',
                raw_scores=True, consumption_preferences=True)
        with open("Personalities/" + filename + ".txt", 'w+') as file:
            file.write(json.dumps(profile, indent=2))
            
    finalMessage = prettyMessage(filename)
    return finalMessage  
    
    
class Personality:
    
    def __init__(self, bot):
        self.bot = bot       
    
    @commands.command(pass_context=True)
    async def analyze(self, ctx, username):
        channelID = ctx.message.channel.id
        channelToGetData = self.bot.get_channel("170682390786605057") #always General
        username = username.strip("<>@!")
        if channelID in textChatIDlist:
            await utils.buildDatabase(username, channelToGetData, self.bot)
            message = getPersonalityJSON(username)
            partOneMark = message.index("Purchasing Preferences")
            partTwoMark = message.index("Movie Preferences")
            #-2 for discord __ underline formatting
            await self.bot.say(message[:partOneMark-2])
            await self.bot.say(message[partOneMark-2:partTwoMark-2])
            await self.bot.say(message[partTwoMark-2:])
