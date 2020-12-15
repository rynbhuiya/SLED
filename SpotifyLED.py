import io
import msvcrt
import os
import select
import sys
import time
from urllib.request import urlopen


import colour
import spotipy
import spotipy.util as util
from colorthief import ColorThief
from PIL import ImageColor
from govee_api import api, device
#from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth

def hex_to_rgb(hex):
    print(hex)
    val = str(hex)
    #val = val.replace('#', '')
    val = val.strip('#')
    if hex == None:
        return (0, 0, 0)
    return tuple(int(val[i:i+2], 16) for i in (0, 2, 4))

def temp_hex_to_rgb(hex):
    print(hex)
    if hex == None:
        return (0, 0, 0)
    val = str(hex)
    val = val.replace('#', '')
    return ImageColor.getcolor(hex, "RGB")

def main():
    # Govee Login
    govee_cli = api.Govee('dinghisk@gmail.com', 'rynsbn02', '10f26ce547a6e781a0c51ed092cd5588')
    govee_cli.login()
    govee_cli.update_device_list() # Gets connected devices

    for dev in govee_cli.devices.values():
        light = dev

    # Get current rgb value of led 
    currHex = light.color
    time.sleep(1)
    currHex = light.color
    time.sleep(1)
    currHex = light.color
    currRGB = hex_to_rgb(currHex)
    old_rgb = currRGB

    # Spotify Login
    scope = 'user-read-currently-playing'
    clientID = 'e2f06877a2fb4407ac2de5db6b2d450e'
    clientSecret = 'b1a86a728c354084b5e26996a79d8ff8'
    token = util.prompt_for_user_token('rynbhuiya', scope, clientID, clientSecret, 'http://localhost')
    sp = spotipy.Spotify(auth=token)


    track = sp.current_user_playing_track() # Grabs info on currently playing track
    try:
        url = track['item']['album']['images'][0]['url'] # Gets the url for the album art
        # ColorThief 
        img = urlopen(url)
        f = io.BytesIO(img.read())
        color = ColorThief(f)
        rgb = color.get_color(quality=3) # Gets the dominant color of the album art
    except TypeError or UnboundLocalError:
        rgb = currRGB

    if(currRGB != rgb):
        light.color = rgb
        old_rgb = rgb
    time.sleep(1)
    
    # Loop exits when user enters esc
    print('Press "esc" to exit program')
    while 1:
        #time.sleep(1) # When switching songs frequently the program would crash - waiting 1s would prevent that 
        track = sp.current_user_playing_track() # Grabs info on currently playing track
        try:
            url = track['item']['album']['images'][0]['url'] # Gets the url for the album art
            img = urlopen(url)
            f = io.BytesIO(img.read())
            color = ColorThief(f)
            rgb = color.get_color(quality=3)
        except TypeError or UnboundLocalError:
            pass

        if (light.on == False):
            light.on = True
            time.sleep(1)
            light.on = True
            time.sleep(1)
            light.on = True
            time.sleep(1)

        if (rgb != old_rgb):
            try:
                light.color = rgb
            except TypeError:
                pass
        #time.sleep(1)
        old_rgb = rgb

        if msvcrt.kbhit():
            if ord(msvcrt.getch()) == 27:
                break

if __name__ == '__main__':
    main()