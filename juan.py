# JJJJJJJJJJJJJ       UU          UU               AAAAAA             NN            NN
#       JJ            UU          UU              AA    AA            NNNN          NN
#       JJ            UU          UU             AA      AA           NN  NN        NN
#       JJ            UU          UU            AA        AA          NN    NN      NN
#       JJ            UU          UU           AAAAAAAAAAAAAA         NN      NN    NN
#       JJ            UU          UU          AA            AA        NN        NN  NN
#      JJ             UU          UU         AA              AA       NN          NNNN
#  JJJJJ              UUUUUUUUUUUUUU        AA                AA      NN            NN
#
# © Copyright YuCode! developers 2020

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
# when the bot started running, we may print its name, id etc
async def on_ready():
    print('Logged in')
    print("Username: ", end='')
    print(client.user.name)
    print("Userid: ", end='')
    print(client.user.id)

@client.event
# when the bot gets a message this method gets triggered
async def on_message(message):
    if message.author.id == client.user.id:
        return

    if message.content.lower() in ['hi', 'hola', 'hello'] :
        list = [
        'Hello {0.author.mention} welcome man, cómo andás my friend?',
        'Hola, {0.author.mention}, how you doing!',
        'Nice to meet you {0.author.mention}'
        ]
        msg = list[random.randint(0, len(list) - 1)].format(message)
        await message.channel.send(msg)

    elif message.content.lower() in ['help', 'ayuda']:
        list = [
        'Let me check with that level and come back to you, amigo!',
        'how can i help you, my friend?',
        'well, i\'m a horse, not sure if i can do more than a human',
        'callate hay gente en africa mucho peor que tu, seguro que tu problema no es tan importante'
        ]
        msg = list[random.randint(0, len(list) - 1)].format(message)
        await message.channel.send(msg)

    # sends a random advice
    elif message.content.lower() in ['random advice', 'tell me something', 'what should i do', 'dime algo', 'un consejo', 'cuentame algo', 'no se que hacer', 'i don\'t know what to do']:
        list = [
        'Eat tacos and be happy!',
        'Horses are nice, i love horses and you should too, compadre',
        'study more, do some exercise and that stuff',
        'burritos are the best, buddy',
        'aw sh*t, here we go again...',
        'reject modernity, embrace juanismo',
        'live and let day, man',
        'yo no sé qué quieres que te diga solo soy juan',
        'no te comas esa burguer',
        'you should always unplug the roaster, trust me'
        ]
        msg = list[random.randint(0, len(list) - 1)].format(message)
        await message.channel.send(msg)

    elif message.content.lower() in ['what language do you speak', 'what languages do you speak', 'que idioma hablas', 'que idiomas hablas']:
        list = ['English, español, a bit of french, some german... But yeah, you know, I\'m Juan, so mainly Spanglish.']
        msg = list[random.randint(0, len(list) - 1)].format(message)
        await message.channel.send(msg)

    elif message.content.lower() in ['who did you vote for', 'who you voted', 'who did you vote', 'who to vote', 'trump or biden']:
        list = [
        'If I told you I would be removed from the server',
        'American Communist Party, cause I just wanted free stuff, like... you know... an iPhone 12 and my daily Starbucks #BLM coffee cup',
        'National Socialist Movement, but please, dont tell my mom :)',
        '#BidenHarris2020... because I like kids. I don\'t know who will be the VP after Joe... you know...',
        'I\'m a horse and my name is juan, so #LatinosForTrump obviously, RIGGED ELECTION!!!!!!! STOP THE COUNT!!!!!',
        'Green Party, like (weed) my meals... #ClimateActionNow!',
        'Jo Jorgensen (L), horses dont deserve taxes nor obligations TAXATION IS THEFT!! END THE WAR ON DRUGS!! GUNS FOR EVERYONE!!',
        '*political compass memes intensify*'
        'Juanist Horse\'s Party, the best party, amigo!'
        ]
        msg = list[random.randint(0, len(list) - 1)]
        await message.channel.send(msg)

    elif message.content.lower() in ['ok?', 'alright?', 'is everything ok?']:
        list = ['ok', 'sure', 'right', 'juanismo']
        msg = list[random.randint(0, len(list) - 1)]
        await message.channel.send(msg)

    # random integer 1 to 100
    elif message.content.lower() in ['random number', 'random number 10', '1 to 10']:
        msg = random.randint(0, 10)
        await message.channel.send(msg)

    # random integer 1 to 100
    elif message.content.lower() in ['random number 100', '1 to 100']:
        msg = random.randint(0, 100)
        await message.channel.send(msg)

    # random ge
    elif str(message.content).lower() in ['random percentage', 'percentage'] or str(['likely', 'odds']) in str(message.content).lower():
        msg = str(round(random.uniform(0, 100), 2)) + '%'
        await message.channel.send(msg)

    # random integer 1 to 1000
    elif message.content.lower() in ['random number 1000', '1 to 1000']:
        msg = random.randint(0, 1000)
        await message.channel.send(msg)

    # yes or no
    elif str(message.content).lower() in ['yes or no', 'yes or no?'] or ('should' in str(message.content).lower()) or str(message.content).lower().startswith('!yn'):
        list = ['YES', 'NO']
        msg = list[random.randint(0, 1)]
        await message.channel.send(msg)

    # sends a random juan gif
    elif message.content.lower() in ['juan']:
        list = [
        'https://i1.kym-cdn.com/entries/icons/original/000/012/837/31947478577132381_uISnEynS_f.jpg',
        'https://i3.kym-cdn.com/photos/images/original/000/546/384/342.png',
        'https://www.thepubliceditor.com/wp-content/uploads/2017/09/Hispanica_Dons_Juan_Meme_05.jpg',
        'https://i.ytimg.com/vi/t5hIhRRc1mQ/hqdefault.jpg',
        'https://i3.kym-cdn.com/photos/images/newsfeed/000/527/379/2fc.jpg',
        'https://s2.quickmeme.com/img/b2/b22e3d52b3480cd345c51b956bbfa3e879b7ba99034561ddcb34a6d9a436369d.jpg',
        'https://sayingimages.com/wp-content/uploads/juan-does-not-simply-burrito-meme.png',
        'https://pics.onsizzle.com/juan-small-step-for-man-mexican-word-ay-comte-juan-2867786.png',
        'https://pics.onsizzle.com/i-hate-tacos-said-no-juan-ever-16074307.png',
        'https://www.memecreator.org/static/images/memes/3861823.jpg',
        'https://i.imgflip.com/ve0m1.jpg', 'https://i.ytimg.com/vi/SFvuAq2upO4/maxresdefault.jpg',
        'https://www.funnybeing.com/wp-content/uploads/2017/05/May-The-Horse-Be-With-You.jpg',
        'https://img.memecdn.com/xbox-juan_o_1541015.jpg',
        'http://memecrunch.com/meme/9QYA/juan-hundred-and-juan-dalmatians/image.jpg?w=1024&c=1'
        ]
        msg = list[random.randint(0, len(list) - 1)].format(message)
        await message.channel.send(msg)

# the bot's token is saved in a seperate module for security reasons. Fool me once, shame on you; fool me twice, shame on me. Va por tí Antonio del CNI roba tokens.
client.run(config.token)
