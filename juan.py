# JJJJJJJJJJJJJ       UU          UU               AAAAAA             NN            NN
#       JJ            UU          UU              AA    AA            NNNN          NN
#       JJ            UU          UU             AA      AA           NN  NN        NN
#       JJ            UU          UU            AA        AA          NN    NN      NN
#       JJ            UU          UU           AAAAAAAAAAAAAA         NN      NN    NN
#       JJ            UU          UU          AA            AA        NN        NN  NN
#      JJ             UU          UU         AA              AA       NN          NNNN
#  JJJJJ              UUUUUUUUUUUUUU        AA                AA      NN            NN

import os
import discord
import config
# from dotenv import load_dotenv

# load_dotenv()
# TOKEN = os.getenv(config.token)

client = discord.Client()

@client.event
#when the bot started running, we may print its name, id etc
async def on_ready():
    print('Logged in')
    print("Username: ", end='')
    print(client.user.name)
    print("Userid: ", end='')
    print(client.user.id)
@client.event
#when the bot gets the message this method gets triggered
async def on_message(message):
    if message.author.id == client.user.id:
        return
    #message starts with hi or hello then print these
    # LOOKING FORWARD TO SOLVING CASE SENSITIVE PROBLEM!
    if message.content.startswith('hi') or message.content.startswith('hello'):
        msg = 'Hello {0.author.mention} welcome man, cómo andás my friend?'.format(message)
        await message.channel.send(msg)
    #when the message with help then do this
    elif message.content.startswith('help'):
        msg = 'Let me check with that level and come back to you, amigo!'.format(message)
        await message.channel.send(msg)

client.run(config.token)
