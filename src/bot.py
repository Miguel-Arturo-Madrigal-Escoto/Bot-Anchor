import discord
from discord.ext import commands
import datetime
from urllib import parse, request
import re
from gtts.tokenizer.core import Tokenizer
from gtts.tokenizer import tokenizer_cases
import os
from youtube_dl import YoutubeDL
import random
from mutagen.mp3 import MP3
from gtts.tts import gTTS
import wikipedia
from discord.utils import get
from googletrans import Translator, constants
import requests
import json, pprint
from _datetime import date


i = discord.Intents.default()
i.members = True
bot = commands.Bot(command_prefix='>', description='Soy el Bot Anchor :)', intents=i)

# ! eliminar commando help default
bot.remove_command('help')

@bot.command()
async def hi(ctx):
    await ctx.send(f'Hola {ctx.message.author.mention}. Saca los apuntadores perro')

@bot.command()
async def delete(ctx):
    await ctx.send(f'Memoria liberada {ctx.message.author.mention}.')

@bot.command()
async def info(ctx):
    now = datetime.datetime.now()
    
    embed = discord.Embed(title=f'{ctx.guild.name}', description='El bot anchor te ayudará en el servidor :)',
                          timestamp=datetime.datetime.utcnow(), color=random.randint(0, 0xffffff))
    embed.set_author(name=f'{ctx.guild.owner}', url='https://phantom-marca.unidadeditorial.es/3eb18f02c50d1d41b33b9daf63105836/resize/1320/f/jpg/assets/multimedia/imagenes/2021/03/05/16149009051163.jpg',
                     icon_url=ctx.author.avatar_url)
    embed.add_field(name='El admin del servidor: ', value=f'{ctx.guild.owner}', inline=True)
    embed.add_field(name='ID del servidor: ', value=f'{ctx.guild.id}', inline=True)
    embed.add_field(name='Región: ', value=f'{ctx.guild.region}', inline=True)
    embed.add_field(name='Fecha de creación: ', value=f'{ctx.guild.created_at}', inline=True)
    embed.add_field(name='Cantidad de miembros', value=f'{ctx.guild.member_count}', inline=True)
    embed.set_thumbnail(url=f'{ctx.guild.icon_url}')
    embed.set_image(url='https://miro.medium.com/max/489/0*WXcNzcCdNpXU4eVw.jpg')
    embed.set_footer(text=f'{now.year} - Todos los derechos reservados')

    await ctx.send(embed=embed)


@bot.command()
async def youtube(ctx, *, search):
    criteria = search.split(' ')
    aux = criteria[1:]
    to_search = ''.join(k for k in aux)

    query = parse.urlencode({'search_query': to_search})
    html_content = request.urlopen('http://www.youtube.com/results?' + query)
    result_set = re.findall( r"watch\?v=(\S{11})", html_content.read().decode())
    
    for i in range(int(criteria[0])):
        try:
            await ctx.send(f'https://www.youtube.com/watch?v={result_set[i]}')
        except:
            await ctx.send(f'No pude encontrar mas videos :(')
            break


@bot.command(pass_context=True)
async def help(ctx):
    autor = ctx.message.author

    embed = discord.Embed( 
                        description='Anchor es un bot multipróposito, el cuál te ayudará a facilitarte ciertas \
                        tareas diriarias y las hará más divertidas.\nEste menu de ayuda te dará a conocer los commandos que Anchor puede usar.', 
                        color=random.randint(0, 0xffffff))
    
    embed.set_author(name=f'Anchor is Love, Anchor is Life',
                    icon_url='https://img.icons8.com/fluent/452/get-help.png')
    embed.add_field(name='>hola', value='Recibir un saludo de Anchor', inline=False)
    embed.add_field(name='>info', value='Consulta la información del servidor', inline=False)
    embed.add_field(name='>youtube n palabras_clave', value='Anchor realiza una búsqueda de "n" videos en YouTube de las palabras_clave', inline=False)
    embed.add_field(name='>play cancion', value='Anchor reproduce la canción proporcionada', inline=False)
    embed.add_field(name='>pause', value='Pausa la canción en reproducción', inline=False)
    embed.add_field(name='>stop', value='Detiene la canción en reproducción', inline=False)
    embed.add_field(name='>resume', value='Continua la reproducción de la canción', inline=False)
    embed.add_field(name='>say idioma texto', value='Anchor repite lo escrito en el idioma especificado\n \
        en: ingles\n    es: español\n   fr: francés\n   zh-CN: chino mandarín\n    pt: portugués', inline=False)
    embed.add_field(name='>define palabras_clave', value='Anchor busca en google la definicion de las palabras clave', inline=False)
    embed.add_field(name='>translate idioma_origen idioma_destino', value='Anchor traduce lo escrito con los idiomas especificados\n \
        Los idiomas soportados son: https://cloud.google.com/translate/docs/languages', inline=False)
    embed.add_field(name='>fshop', value='Anchor muestra la tienda actual de Fortnite', inline=False)
    embed.add_field(name='>fstats usuario', value='Anchor consulta las estadísticas de Fortnite del usuario', inline=False)

    await ctx.send(embed=embed)

@bot.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    voice_channel = discord.utils.get(ctx.guild.voice_channels, name=channel.name)
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice is None:
        voice = await voice_channel.connect()
    else:
        await ctx.send('Ya estoy connectado al canal') 

@bot.command()
async def leave(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice is not None:
        voice = await voice.disconnect()
    else:
        await ctx.send('No estoy conectado a ningun canal')

def audio_len(path):
    global MP3
    audio = MP3(path)
    return(audio.info.length)


@bot.command()
async def say(ctx, *, text):
    global gTTS
    txt = text.split(' ')
    say = txt[1:]
    texto = ' '.join(k for k in say)

    try:
        speech = gTTS(text=texto, lang=txt[0], slow=False, tokenizer_func=Tokenizer([tokenizer_cases.tone_marks, tokenizer_cases.period_comma, tokenizer_cases.colon, tokenizer_cases.other_punctuation]).run)
        speech.save('audio.mp3')
        
        channel = ctx.author.voice.channel
        voice_channel = discord.utils.get(ctx.guild.voice_channels, name=channel.name)
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

        if voice is None:
            voice = await voice_channel.connect()
        
        voice.play(discord.FFmpegPCMAudio('audio.mp3'), after=lambda e: print('done'))
    except:
        await ctx.send('El lenguaje proporcionado es invalido y/o no soportado :(')


@bot.command()
async def play(ctx, *, search):
    query = parse.urlencode({'search_query': search})
    html_content = request.urlopen('http://www.youtube.com/results?' + query)
    result_set = re.findall(r"watch\?v=(\S{11})", html_content.read().decode())
    
    try:
        os.remove('cancion.m4a')
    except FileNotFoundError:
        # archivo no encontrado
        pass

    audio_downloader = YoutubeDL({'format':'bestaudio', 'outtmpl':'cancion.m4a'})
    audio_downloader.extract_info(result_set[0])

    #os.system('youtube-dl --rm-cache-dir')

    channel = ctx.author.voice.channel
    voice_channel = discord.utils.get(ctx.guild.voice_channels, name=channel.name)
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if voice == None:
        voice = await voice_channel.connect()
    
    await ctx.send(f'https://www.youtube.com/watch?v={result_set[0]}')
    voice.play(discord.FFmpegPCMAudio('cancion.m4a'), after=lambda e: print('done'))


@bot.command()
async def stop(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    voice.stop()


@bot.command()
async def pause(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice is not None and voice.is_playing():
        voice.pause()
    else:
        await ctx.send('No hay canciones reproduciendose actualmente ')

@bot.command()
async def resume(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send('El audio no esta en pausa')

def wiki_summary(arg):
    search = definition = None
    try:
        try:
            try:
                search = wikipedia.search(arg, suggestion=False, results=5)
            except:
                search = wikipedia.search(arg, suggestion=False, results=1)

            definition = wikipedia.summary(arg, sentences=3, chars=1000, auto_suggest=False, redirect=True)
            return definition

        except wikipedia.DisambiguationError as e:
            search = wikipedia.search(arg, suggestion=False, results=5)
            return search
    except wikipedia.PageError:
        return None

@bot.command()
async def translate(ctx, *arg):
    try:
        translator = Translator()
        src = arg[0]
        dest = arg[1]
        msg = arg[2:]
        msg = ' '.join(k for k in msg)

        msg = translator.translate(msg, dest=dest, src=src)
        e = discord.Embed(description=msg.text, color=random.randint(0, 0xffffff))
        e.set_author(name='Resultados de la Traducción',
                    icon_url='https://upload.wikimedia.org/wikipedia/commons/d/db/Google_Translate_Icon.png')
        await ctx.send(embed=e)
        
    except:
        await ctx.send('Parametros de traducción inválidos')


@bot.command()
async def define(ctx, *, search):
    pass

@bot.command()
async def fshop(ctx):
    e = discord.Embed(color=random.randint(0, 0xffffff), description='https://fnbr.co/shop')
    e.set_author(name='Fortnite Shop', icon_url='https://www.epicgames.com/fortnite/es-ES/creative/docs/Images/placeholder-topic.jpg')
    e.set_image(url='https://fortool.fr/cm/assets/shop/en.png')

    await ctx.send(embed=e)

@bot.command()
async def fstats(ctx, username):
    request_url = f'https://fortnite-api.com/v1/stats/br/v2?name={username}'
    now = date.today()

    stats = json.loads(requests.get(
        request_url,
        params={
            'displayName': username
        }
    ).content)
    e = None
    try:
        stats = stats['data']
        for key in stats:
            if key == 'account':
                stats['account'] = stats['account']['name']

        aux = {}
        aux['battlePass'] = stats['battlePass']
        stats = stats['stats']['all']['overall']
        stats.update(aux)
        #xd = pprint.pformat(stats, indent=4, width=80)
        e = discord.Embed(color=random.randint(0, 0xffffff), description=f'Se proporcionan las estadísticas de Fortnite del usuario "{username}"')
        e.set_author(name='Fortnite Stats', icon_url='https://www.epicgames.com/fortnite/es-ES/creative/docs/Images/placeholder-topic.jpg')
        e.set_footer(text=f'Las estadisticas son vigentes a la fecha {now}')
        for key in stats:
            if key != 'battlePass':
                e.add_field(name=key, value=stats[key], inline=True)
            else:
                e.add_field(name=f'battlePass level', value=stats[key]['level'], inline=True)  
    except:
        e = discord.Embed(color=random.randint(0, 0xffffff), description=f'No se pudieron encontrar las estadísticas de Fortnite del usuario "{username}"')
        e.set_author(name='Fortnite Stats', icon_url='https://www.epicgames.com/fortnite/es-ES/creative/docs/Images/placeholder-topic.jpg')
        e.set_footer(text=f'Las estadisticas son vigentes a la fecha {now}')
    finally:
        await ctx.send(embed=e)


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Streaming(name='Estoy haciendo el religado', url='https://www.twitch.tv/directory'))
    print('Anchor is ready')

@bot.event
async def on_message(message):
    words = message.content.split()
    important = words[1:]

    if str(message.channel) == 'memes' and message.content != '':
        await message.channel.purge(limit=1)

    elif message.content.startswith('>define'):
    
        words = message.content.split()
        important = words[1:]

        definition = wiki_summary(important)

        if definition is not None:
            translator = Translator()
            if not isinstance(definition, list):  
                definition =  translator.translate(definition, dest='es', src='en')
                e = discord.Embed(description=definition.text, color=random.randint(0, 0xffffff))
                e.set_author(name='Resultados de la Búsqueda',
                        icon_url='https://rotulosmatesanz.com/wp-content/uploads/2017/09/2000px-Google_G_Logo.svg_.png')

                await message.channel.send(embed=e)
            else:
                e = discord.Embed(description='Se ha encontrado más de 1 coincidencia en la búsqueda proporcionada.', color=random.randint(0, 0xffffff))
                e.set_author(name='Resultados de la Búsqueda',
                        icon_url='https://rotulosmatesanz.com/wp-content/uploads/2017/09/2000px-Google_G_Logo.svg_.png')
                
                #definition = [k for k in definition if k is not None]
                for busq in definition:
                    try:
                        definition = wikipedia.summary(busq, sentences=3, chars=1000, auto_suggest=False, redirect=True)
                        definition =  translator.translate(definition, dest='es', src='en')

                        aux = busq
                        aux = translator.translate(busq, dest='es', src='en')
                        e.add_field(name=aux.text, value=definition.text, inline=False)
                    except:
                        pass

                await message.channel.send(embed=e)
        
        else:
            aux = ' '.join(k for k in important)
            e = discord.Embed(description=f'No se encontraron resultados para la búsqueda: "{aux}".', color=random.randint(0, 0xffffff))
            e.set_author(name='Resultados de la búsqueda',
                        icon_url='https://rotulosmatesanz.com/wp-content/uploads/2017/09/2000px-Google_G_Logo.svg_.png')
            await message.channel.send(embed=e)
    await bot.process_commands(message)


@bot.event
async def on_reaction_add(reaction, user):
    channel = reaction.message.channel
    await channel.send(f'{user.name} ha añadido {reaction.emoji} a {reaction.message.content}')

@bot.event
async def on_reaction_remove(reaction, user):
    channel = reaction.message.channel
    await channel.send(f'{user.name} ha quitado {reaction.emoji} a {reaction.message.content}')

#keep_alive()
bot.run('ODYwMDAxNzkwMjI1NTQ3MjY0.YN05FA.iNf8yvgIacF3NxmKJDSbEv13aFk')


