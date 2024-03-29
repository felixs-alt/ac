import os, python_weather, asyncio, sys, time, aiohttp, requests, random
from dotenv import load_dotenv
from datetime import datetime
from colorama import Fore, Style, init
from pytz import timezone
from threading import Thread
import pytz
init()

load_dotenv()
game = "Animal Crossing: New Horizons"
def b(text: str):
    return Fore.BLUE + text + Style.RESET_ALL
def g(text: str):
    return Fore.GREEN + text + Style.RESET_ALL
def p(text: str):
    return Fore.MAGENTA + text + Style.RESET_ALL
def o(text: str):
    return Fore.ORANGE + text + Style.RESET_ALL
def c(text: str):
    return Fore.CYAN + text + Style.RESET_ALL


if not os.path.exists(".env"):
    print("\nTo run, we need to use " + b("dotenv") + " to get your location. There should be a file called " + b("'.env'") + "in the same directory as " + b("'play.py'") + ". Read the README.md for more information.")
    sys.exit(0)



volume = int(os.getenv("VOLUME"))
area = str(os.getenv("AREA"))
roost = str(os.getenv("ROOST"))
games = requests.get(f"https://cloud.oscie.net/acdp/list.json").json()


if roost == "True" and os.path.exists("./files/roost.mp3"):
    playroost = True
else:
    playroost = False
    

async def videoDL(outfile, url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                with open(outfile, "wb") as f:
                    async for data in response.content.iter_chunked(1024):
                        f.write(data)
    except Exception as e:
        print(f"**`ERROR:`** {type(e).__name__} - {e}")
    downloadedaudio=True


def pocketcalc(hour:str):

    if hour == "00" or hour == "01" or hour == "02" or hour == "03" or hour == "04" or hour == "22" or hour == "23":
        return "night"
    elif hour == "05" or hour == "06" or hour == "07" or hour == "08" or hour == "09" or hour == "10" or hour == "11":
        return "morning"
    elif hour == "12" or hour == "13" or hour == "14" or hour == "15" or hour == "16":
        return "day"
    elif hour == "17" or hour == "18" or hour == "19" or hour == "20" or hour == "21":
        return "evening"
    else:
        return "campsite"


async def getweather():
    async with python_weather.Client(format=python_weather.IMPERIAL) as client:
        weather = await client.get(area)

        global sky
        sky = weather.current.description

        await client.close()


async def gamecheck():
    getweather()
    global downloadedaudio
    global playcount
    playcount = 0

    print("Checking for games...")

    
    while True:
        
        if game == "Animal Crossing":
            if "snow" in sky or "Snow" in sky or "snowy" in sky or "Snowy" in sky:
                gameweather = "snow"
            else:
                gameweather = "clear"
        else:
            if "snow" in sky or "Snow" in sky or "snowy" in sky or "Snowy" in sky:
                gameweather = "snow"
            elif "Rain" in sky or "rain" in sky or "rainy" in sky or "Rainy" in sky or "Mist" in sky or "mist" in sky or "shower" in sky or "Shower" in sky:
                gameweather = "rain"
            else:
                gameweather = "clear"

        gametime = random.randint(1,24)

        print(Style.RESET_ALL + "[" + datetime.now(pytz.timezone('Europe/Copenhagen')).strftime(c('%H:%M - %d/%m')) + "] " + b(sky) + Fore.YELLOW)

        if game == "Animal Crossing: Pocket Camp":
            dir = f"./files/{pocketcalc(gametime)}.mp3"
        else:
            if playroost == True:
                rack = random.randint(1, 1000)
                if rack == 5:
                    dir = "./files/roost.mp3"
                else:
                    dir = f"./files/{gameweather}/{gametime}.mp3"
            else:
                dir = f"./files/{gameweather}/{gametime}.mp3"
        os.system(f"curl -o main.mp3 https://cloud.oscie.net/acdp/acnh/{gameweather}/{gametime}.mp3")
        playcount = playcount + 1
        os.system(f"ffmpeg -i  main.mp3 -listen 1 -method GET -c copy -f MP3 http://0.0.0.0:5000/main.mp3")
async def downloader_menu():

    gameslist = []

    for game in games['available']:
        gameslist.append(game['shortname'])

    print("\nWelcome to the " + p("ACDP") + " (" + p("Animal Crossing Dynamic Player") + ") music downloader.\nIf you're seeing this, " + c("chances are, you do not have the audio files downloaded.\n") + "\n" + c("Space Requirements:"))

    for game in games['available']:
        print(f"- {g(game['shortname'])} requires ~{b(game['size'])}")

    game = "New Horizons"

    if game not in gameslist:
        print(Style.RESET_ALL + "\n'" + b(game) + "' is not a valid option. Valid options include:\n" + g(str(gameslist).replace("[", "").replace("]", "")) + "\n")
        await downloader_menu()

    for gameitem in games['available']:
        if gameitem['shortname'] == game:
            gamecode = gameitem['code']

    await downloader_game(code=gamecode)

async def downloader_game(code:str):
    
    for gameitem in games['available']:
        if gameitem['code'] == code:
            game = gameitem['name']
            type = gameitem['type']
            roos = gameitem['roost']

    for item in games['unsupported']:
        if code == item['code']:
            print(Style.RESET_ALL + "\n" + g(game) + " is currently unsupported, sorry!")
            sys.exit(0)

    print(Style.RESET_ALL + "\n\nDownload started for " + g(game) + "!\n")

    Style.RESET_ALL

    if os.path.exists("./files/rain/"):
        print(Style.RESET_ALL + "If there are " + b("audio files") + " in the 'files/[weather]' folders, " + c("this may not work") + ".\nPlease make sure there are " + b("no files in them before continuing.") + "\nThis may take a while, please wait...\n")

    if type == "norain":

        for i in range (24):
            if len(str(i)) == 1:
                num = f"0{i}"
            else:
                num = i
            await videoDL(outfile = f"./files/snow/{num}.mp3", url = f"https://cloud.oscie.net/acdp/{code}/snow/{num}.mp3")
            print("Downloading " + b("Snow ") + "(" + b(str(i)) + ")...")

        for i in range (24):
            if len(str(i)) == 1:
                num = f"0{i}"
            else:
                num = i
            await videoDL(outfile = f"./files/clear/{num}.mp3", url = f"https://cloud.oscie.net/acdp/{code}/clear/{num}.mp3")
            print("Downloading " + b("Clear ") + "(" + b(str(i)) + ")...")

    elif type == "periodic":

        tracklist = ["campsite", "morning", "day", "evening", "night"]

        for track in tracklist:
            await videoDL(outfile = f"./files/{track}.mp3", url = f"https://cloud.oscie.net/acdp/{code}/{track}.mp3")
            print("Downloading " + b(track.capitalize()) + "...")

    else:

        for i in range (24):
            if len(str(i)) == 1:
                num = f"0{i}"
            else:
                num = i
            await videoDL(outfile = f"./files/rain/{num}.mp3", url = f"https://cloud.oscie.net/acdp/{code}/rain/{num}.mp3")
            print("Downloading " + b("Rain ") + "(" + b(str(i)) + ")...")

        for i in range (24):
            if len(str(i)) == 1:
                num = f"0{i}"
            else:
                num = i
            await videoDL(outfile = f"./files/snow/{num}.mp3", url = f"https://cloud.oscie.net/acdp/{code}/snow/{num}.mp3")
            print("Downloading " + b("Snow ") + "(" + b(str(i)) + ")...")

        for i in range (24):
            if len(str(i)) == 1:
                num = f"0{i}"
            else:
                num = i
            await videoDL(outfile = f"./files/clear/{num}.mp3", url = f"https://cloud.oscie.net/acdp/{code}/clear/{num}.mp3")
            print("Downloading " + b("Clear ") + "(" + b(str(i)) + ")...")

    if roos == True:
        await videoDL(outfile = "./files/roost.mp3", url = f"https://cloud.oscie.net/acdp/{code}/roost.mp3")
        print("Downloading " + b("Roost") + "...")

    with open("./files/name.txt", "x") as f:
        f.write(game)

    print(c("Done downloading") + "! Your " + b("music") + " should start quickly!\n")


async def main():
    print("\nWelcome to the " + p("Animal Crossing Dynamic Player") + "!\nThe " + p("ACDP") + " lets you listen to " + g("Animal Crossing") + " games' music based around the " + b("weather") + " and " + b("time") + " around you.\n")

    await getweather()
    await gamecheck()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(c("\n\nExiting program...\n"))
        print("While using this app, you listened to the music " + b(str(playcount)) + " times!")


        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
