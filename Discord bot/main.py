import speech_recognition
import pyttsx3
import requests
import discord
from discord.ext import commands
import yt_dlp
import os
import sys

recognizer = speech_recognition.Recognizer()


TOKEN = 
intents = discord.Intents.default()
intents.message_content = True
#client = discord.Client(intents=intents)
client = commands.Bot(command_prefix= '$', intents=intents)

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
        'preferredquality': '192',
    }],
}


@client.event
async def on_ready():
    print("ready!")
    for file in os.listdir("./"):
        if file.endswith(".wav"):
            os.remove(file)

@client.command(pass_context = True, name="generate image from text" , aliases = ["g"])
async def generate(ctx, arg):
    r = requests.post(
        "https://api.deepai.org/api/text2img",
        data={
            'text': arg,
        },
        headers={'api-key': 'quickstart-QUdJIGlzIGNvbWluZy4uLi4K'}
    )

    try:
        await ctx.send(r.json()["output_url"])

    except Exception as e:
        print(r.json())

@client.command(pass_context = True, name="generate image from audio" , aliases = ["gyt"])
async def generateD(ctx, arg):
    recognizer = speech_recognition.Recognizer()
    ydl = yt_dlp.YoutubeDL(ydl_opts)
    ydl.download(str(arg))
    for file in os.listdir("./"):
        if file.endswith(".wav"):
            os.rename(file, "audio.wav")
            arg = "audio.wav"
    try:
        await ctx.send("Listening...")
        print('step1')
        with speech_recognition.WavFile("audio.wav") as source:
            audio = recognizer.record(source)
            print('step2')
            text = recognizer.recognize_google(audio)
            text = text.lower()
            print('step3')
            await ctx.send("Generating an image for: " + str(text))
            print('step4')
            r = requests.post(
                "https://api.deepai.org/api/text2img",
                data={
                    'text': text,
                },
                headers={'api-key': '111b1cd1-abed-4691-9422-dfdfcf818cad'}
            )
            print('step5')
            try:
                await ctx.send(r.json()["output_url"])

            except Exception as e:
                await ctx.send(r.json())

        for file in os.listdir("./"):
            if file.endswith(".wav"):
                os.remove(file)

    except Exception as e:
        print(e)
        recognizer = speech_recognition.Recognizer()

@client.command(pass_context = True , name = "restart", help="restart")
async def restart(ctx):
    print("argv: " , sys.argv)
    print("sys executable: " ,sys.executable)
    print("restart now")
    await ctx.send("restarting the bot")
    os.execv(sys.executable, ['python'] + sys.argv)

client.run(TOKEN)