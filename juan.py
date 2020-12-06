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
        answers = [
        'Hello {0.author.mention} welcome man, cómo andás my friend?',
        'Hola, {0.author.mention}, how you doing!',
        'Nice to meet you {0.author.mention}'
        ]
        msg = random.choice(answers).format(message)
        await message.channel.send(msg)

    elif message.content.lower() in ['help', 'ayuda']:
        answers = [
        'Let me check with that level and come back to you, amigo!',
        'how can i help you, my friend?',
        'well, i\'m a horse, not sure if i can do more than a human',
        'callate hay gente en africa mucho peor que tu, seguro que tu problema no es tan importante'
        ]
        msg = random.choice(answers).format(message)
        await message.channel.send(msg)

    # sends a random advice
    elif message.content.lower() in ['random advice', 'tell me something', 'what should i do', 'dime algo', 'un consejo', 'cuentame algo', 'no se que hacer', 'i don\'t know what to do']:
        answers = [
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
        msg = random.choice(answers).format(message)
        await message.channel.send(msg)

    elif ('language', 'speak', 'idioma') in message.content.lower():
        answers = ['English, español, a bit of french, some german... But yeah, you know, I\'m Juan, so mainly Spanglish.']
        msg = random.choice(answers).format(message)
        await message.channel.send(msg)

    elif ('nadie te preguntó', 'who asked you', 'shut up', 'pesado') in message.content.lower():
        answers = [
        'tampoco hace falta insultar eh',
        'hey I\'m a horse, be patient',
        'I guess if you were a horse, you coudn\'t be as smart as I am',
        'God sent me!'
        '#RESPECT bruh'
        ]
        msg = random.choice(answers).format(message)
        await message.channel.send(msg)

    elif ('vote', 'trump or biden', 'biden or trump') in message.content.lower():
        answers = [
        'If I told you I would be removed from the server',
        'American Communist Party, cause I just wanted free stuff, like... you know... an iPhone 12 and my daily Starbucks #BLM coffee cup',
        'National Sociaanswers Movement, but please, dont tell my mom :)',
        '#BidenHarris2020... because I like kids. I don\'t know who will be the VP after Joe... you know...',
        'I\'m a horse and my name is juan, so #LatinosForTrump obviously, RIGGED ELECTION!!!!!!! STOP THE COUNT!!!!!',
        'Green Party, like (weed) my meals... #ClimateActionNow!',
        'Jo Jorgensen (L), horses dont deserve taxes nor obligations TAXATION IS THEFT!! END THE WAR ON DRUGS!! GUNS FOR EVERYONE!!',
        '*political compass memes intensify*'
        'Juanist Horse\'s Party, the best party, amigo!'
        'Falange Española Cabalanswersa de las Juntas de Ofensiva Nacional-Juanistas'
        ]
        msg = random.choice(answers).format(message)
        await message.channel.send(msg)

    elif ('ok', 'sure', 'alright') in message.content.lower():
        answers = ['ok', 'sure', 'right', 'juanismo']
        msg = random.choice(answers).format(message)
        await message.channel.send(msg)

    elif ('not bad', 'better than expected') in message.content.lower():
        answers = [
        'not bad at all buddy',
        'I told you!', 'I\'m the best my friend!',
        'Soy un caballo qué esperabas compadre?'
        ]
        msg = random.choice(answers).format(message)
        await message.channel.send(msg)

    elif ('LGBT') in message.content.lower():
        answers = ['Sorry, I only know about the Large Goats Beating Trees Association, next to my field. They\'re nice goats']
        msg = random.choice(answers).format(message)
        await message.channel.send(msg)

    elif ('QAnon') in message.content.lower():
        answers = ['Horses don\'t have conspiracy theories, so idk what to say, man']
        msg = random.choice(answers).format(message)
        await message.channel.send(msg)

    elif ('who are you', 'your name') in message.content.lower():
        answers = [
        'My name is Juan Benito and I\'m a horse',
        'Mi nombre es Juan Benito y soy un caballo',
        'Sometimes I can be a bit annoying, I know, but I\'m Juan, you know...'
        'A veces puedo ser un poco pesado, lo sé, pero soy Juan'
        'I won\'t tell you haha'
        'I don\'t know who created me, am I someone?'
        ]
        msg = random.choice(answers).format(message)
        await message.channel.send(msg)

    # random integer 1 to 100
    elif message.content.lower() in ['random number', 'random number 10', '1 to 10']:
        msg = random.randint(0, 10)
        await message.channel.send(msg)

    # random integer 1 to 100
    elif message.content.lower() in ['random number 100', '1 to 100']:
        msg = random.randint(0, 100)
        await message.channel.send(msg)

    # random percentage
    elif ('random percentage', 'percentage', 'odds', 'likely') in message.content.lower():  # or ('likely' & 'odds') in str(message.content).lower()):
        msg = (str(round(random.uniform(0, 100), 2)) + '%').format(message)
        await message.channel.send(msg)

    # random integer 1 to 1000
    elif message.content.lower() in ['random number 1000', '1 to 1000']:
        msg = random.randint(0, 1000)
        await message.channel.send(msg)

    # yes or no
    elif message.content.lower().startswith('yes or no') or ('should' in str(message.content).lower()) or str(message.content).lower().startswith('!yn'):
        answers = ['YES', 'NO']
        msg = answers[random.randint(0, 1)]
        await message.channel.send(msg)

    # sends a random juan gif
    elif message.content.lower() in ['juan']:
        answers = [
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
        msg = random.choice(answers).format(message)
        await message.channel.send(msg)

    elif message.content.lower() in ['viva españa', 'viva espana']:
        answers = ['No results found for "Viva España". Did you mean ":flag_es: ARRIBA ESPAÑA :flag_es:" ?']
        msg = random.choice(answers).format(message)
        await message.channel.send(msg)

    elif message.content.lower() in ['arriba españa', 'arriba espana', 'una, grande y libre', 'una grande libre', 'una grande y libre', 'dios patria rey']:
        answers = ['https://finofilipino.org/wp-content/uploads/2020/07/CPmkeAcWwAAo-eF.jpg']
        msg = random.choice(answers).format(message)
        await message.channel.send(msg)

    elif message.content.lower().startswith(('how are you', 'are you ok')):
        answers = [
        'Doing great!',
        'Just fine',
        'Feeling awesome!',
        'Mejor que nunca compadre!'
        ]
        msg = random.choice(answers).format(message)
        await message.channel.send(msg)

# the bot's token is saved in a seperate module for security reasons. Fool me once, shame on you; fool me twice, shame on me. Va por tí Antonio del CNI roba tokens.
client.run(config.token)
