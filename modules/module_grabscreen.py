### Summary

# This module grabs an image from the screen and funnels
# it to the processing module

# -------------------------------------------------

from mss import mss # python3 -m pip install -U --user mss
import cv2 # pip install opencv-python
from PIL import Image # python3 -m pip install Pillow
import numpy as np
import time
import asyncio
from modules import module_process
from modules.config import *
import discord #python3 -m pip install -U discord.py[voice]
from discord.ext import commands
from discord.ext.commands import check
from discord import voice_client
from discord import Role
from discord import Guild
from concurrent.futures import ThreadPoolExecutor

def grabDiscussionTitle(xResolution: int, yResolution: int, bot: commands.bot):
    
    settings = {'top': int(0.08 * yResolution) + adjust_y, 'left':int(xResolution * 0.18) + adjust_x, 'width':int(xResolution * 0.7), 'height':int(0.25 * yResolution)}

    sct = mss()

    first_time = True

    while True:
        #Take image of screen
        sct_img = sct.grab(settings)
        img = Image.frombytes('RGB', (sct_img.size.width, sct_img.size.height), sct_img.rgb)
        frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

        if first_time:
            print("Ready.\nYou can play now.\n")
            first_time = False

        #Process image
        newState = module_process.processDiscussion(frame)
        if newState == 1:
            for member in list(bot.get_all_members()):
                if member.voice == None:
                    pass
                else:
                    print(f"Unmuting: {member}")
                    with ThreadPoolExecutor(max_workers=1) as executor:
                        executor.submit(member.edit(mute = False))
        elif newState == 2:
            for member in list(bot.get_all_members()):
                if member.voice == None:
                    pass
                else:
                    print(f"Muting: {member}")
                    with ThreadPoolExecutor(max_workers=1) as executor:
                        executor.submit(member.edit(mute = True))


def grabEndingScreen(xResolution: int, yResolution: int, bot: commands.bot):
    settings = {'top': int(0.065 * yResolution) + adjust_y, 'left':int(xResolution * 0.22) + adjust_x, 'width':int(xResolution * 0.5), 'height':int(0.13 * yResolution)} 

    sct = mss()

    while True:
        #Take image of screen
        sct_img = sct.grab(settings)
        img = Image.frombytes('RGB', (sct_img.size.width, sct_img.size.height), sct_img.rgb)
        frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

        # time.sleep(1)
        # cv2.imshow('Test', np.array(frame)) #output screen, for testing only

        newState = module_process.processEnding(frame)
        if newState == 1:
            for member in list(bot.get_all_members()):
                if member.voice == None:
                    pass
                else:
                    print(f"Unmuting: {member}")
                    res = member.edit(mute = False)
                    print(res)

        elif newState == 2:
            for member in list(bot.get_all_members()):
                if member.voice == None:
                    pass
                else:
                    print(f"Muting: {member}")
                    res = member.edit(mute = True)
                    print(res)
        # if cv2.waitKey(25) & 0xFF == ord('q'):
        #     cv2.destroyAllWindows()
        #     break

if __name__ == "__main__":
    print("Please run start.py: ")
    exit()
