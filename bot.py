import discord
from discord.ext import commands
import random

bot = commands.Bot(command_prefix='!', description='The official BuckeyeLAN bot')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def commend():
	return

@bot.command()
async def test():
	await bot.say('Test!')

@bot.command()
async def points():
	return

@bot.command()
async def roulette(amount : int):
	return

@bot.command()
async def quote():
	return

@bot.command()
async def catgirl():
	catNumber = random.randint(1, 315)
	catName = catNumber
	if(catNumber == 315):
<<<<<<< HEAD
		await bot.say("BONUS ROUND")
=======
>>>>>>> parent of 737a2c3... #NICE
		bonusCatNumber = random.randint(1, 22)
		catName = 'BONUS' + bonusCatNumber
	imageName = catName + '.jpg'
	await bot.upload(imageName)
	return

@bot.command()
async def husbando():
	return
<<<<<<< HEAD

=======
>>>>>>> parent of 737a2c3... #NICE
