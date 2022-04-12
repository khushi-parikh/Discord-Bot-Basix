import discord
from discord.ext import commands
import random
from PIL import Image,ImageFilter
from io import BytesIO

client = commands.Bot(command_prefix='$')

@client.event   
async def on_ready():
    print('bot is ready')

@client.command()
async def dob(ctx):
    await ctx.send('I was born on 13th February, 2020 and I\'m still smarter than you xD')

h = open('help.txt','r')
help_text = h.readlines()
@client.command(aliases = ['h'])
async def help_me(ctx):
    embed = discord.Embed(color=discord.Colour.red())
    values = {'help_me' : 'returns list of commands',
'hello' : 'welcomes you to the server',
'dob' : 'gives dob of bot',
'clear/c/clr' : 'clears certain amount of msgs',
'pfp/dp (name)' : 'returns pfp ',
'dead (name)' : 'shows how much percent dead you are',
'pixel/pixelate (name)' : 'returns a pixelated image',
'merge/m (name) (name)' : 'merges two images',
'evaluate (name)' : 'exposure/contrast changes, khud hi dekh lo',
'spread (name)' : 'returns a grainy distorted image',
'emboss (name)' : 'creates a grey emboss'}
    for i in values:
        embed.add_field(name = i , value = values[i] , inline = True)
    await ctx.send(embed=embed)
    #for i in help_text:
    #    await ctx.send(i)

@client.command()
async def hello(ctx , *member ):
    await ctx.send('Hello {} !!'.format(' '.join(member)))
    
@client.command(aliases = ['c','clr'])
async def clear(ctx,amount=1):
    await ctx.channel.purge(limit = amount+1)

@client.command()
async def dead(ctx , member:discord.Member):
    embed = discord.Embed(title = member.name , color=discord.Colour.red())
    num = random.randint(0,100)
    embed.add_field(name = 'Dead percent' , value = f"{num} %", inline = True)
    embed.set_thumbnail(url = member.avatar_url)
    await ctx.send(embed=embed)
    
@client.command(aliases=['dp'])
async def pfp(ctx , member:discord.Member):
    #embed = discord.Embed(color=discord.Colour.green())
    #embed.set_thumbnail(url = member.avatar_url)
    #await ctx.send(embed = embed)
    url = member.avatar_url
    await ctx.send(url)

@client.command(aliases=['pixelate'])
async def pixel(ctx , member:discord.Member):
    asset = member.avatar_url_as(size = 256)
    data = BytesIO(await asset.read())
    img = Image.open(data)
    imgSmall = img.resize((25,25),resample=Image.BILINEAR)
    result = imgSmall.resize(img.size,Image.NEAREST)
    result.save('pixelated.jpg')
    await ctx.send(file = discord.File('pixelated.jpg'))

@client.command(aliases=['m'])
async def merge(ctx , *member:discord.Member):
    asset1 = member[0].avatar_url_as(size = 256)
    asset2 = member[1].avatar_url_as(size = 256)
    data1 = BytesIO(await asset1.read())
    data2 = BytesIO(await asset2.read())
    img1 = Image.open(data1)
    img2 = Image.open(data2)
    result = Image.blend(img1,img2,0.5)
    result.save('merged.jpg')
    await ctx.send(file = discord.File('merged.jpg'))

@client.command()
async def evaluate(ctx , member:discord.Member):
    asset = member.avatar_url_as(size = 256)
    data = BytesIO(await asset.read())
    img = Image.open(data)
    result = Image.eval(img, (lambda x: 1000 - x * 10))
    result.save('eval.jpg')
    await ctx.send(file = discord.File('eval.jpg'))

@client.command()
async def spread(ctx , member:discord.Member):
    asset = member.avatar_url_as(size = 256)
    data = BytesIO(await asset.read())
    img = Image.open(data)
    result = Image.Image.effect_spread(self = img,distance=25)
    result.save('eval.jpg')
    await ctx.send(file = discord.File('eval.jpg'))

@client.command()
async def emboss(ctx , member:discord.Member):
    asset = member.avatar_url_as(size = 256)
    data = BytesIO(await asset.read())
    img = Image.open(data)
    result = img.filter(ImageFilter.EMBOSS)
    result.save('eval.jpg')
    await ctx.send(file = discord.File('eval.jpg'))

client.run('key here')