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
import random
import math
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

    if message.content.lower() in ['hi', 'hola', 'hello'] :
        list = ['Hello {0.author.mention} welcome man, cómo andás my friend?', 'Hola, {0.author.mention}, how you doing!', 'Nice to meet you {0.author.mention}']
        msg = list[random.randint(0, len(list) - 1)].format(message)
        await message.channel.send(msg)

    elif message.content.lower() in ['help', 'ayuda']:
        list = ['Let me check with that level and come back to you, amigo!', 'how can i help you, my friend?', 'well, i\'m a horse, not sure if i can do more than a human', 'callate hay gente mucho peor en africa que tu, seguro que tu problema is not that important']
        msg = list[random.randint(0, len(list) - 1)].format(message)
        await message.channel.send(msg)

    elif message.content.lower() in ['random advice', 'tell me something', 'what should i do', 'dime algo', 'un consejo', 'cuentame algo', 'no se que hacer', 'i don\'t know what to do']:
        list = ['Eat tacos and be happy!', 'Horses are nice, i love horses and you should too, compadre', 'study more, do some exercise and that stuff', 'burritos are the best, buddy', 'aw sh*t, here we go again...', 'reject modernity, embrace juanismo', 'live and let day, man', 'yo no sé qué quieres que te diga solo soy juan', 'no te comas esa burguer', 'you should unplug the roaster, trust me']
        msg = list[random.randint(0, len(list) - 1)].format(message)
        await message.channel.send(msg)

    elif message.content.lower() in ['what language do you speak', 'what languages do you speak', 'que idioma hablas', 'que idiomas hablas']:
        msg = 'English, español, a bit of french, some german... But yeah, you know, I\'m Juan, so mainly Spanglish.'
        await message.channel.send(msg)

    elif message.content.lower() in ['who did you vote', 'who to vote', 'trump or biden']:
        list = ['If I told you I would be removed from the server', 'American Communist Party, cause I just wanted free stuff, like... you know... an iPhone 12 and my daily Starbucks #BLM coffee cup', 'National Socialist Movement, but please, dont tell anyone :)', '#BidenHarris2020... well, actually Kamala, because I don\'t know who will be the VP after Joe passes away', 'I\'m a horse and my name is juan, so #LatinosForTrump obviously, RIGGED ELECTION!!!!!!!!!!!!!!!', 'Green Party, like (weed) my meals...', 'Jo Jorgensen (L), horses dont deserve taxes nor obligations', '*political compass memes intensify*']
        msg = list[random.randint(0, len(list) - 1)].format(message)
        await message.channel.send(msg)


client.run(config.token)
