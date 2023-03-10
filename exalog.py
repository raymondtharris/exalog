from pynput import keyboard
from PIL import ImageGrab
from datetime import datetime
from pathlib import Path
import getpass
import pandas as pd
import platform

print(platform.system())
currentPlatform = platform.system()
keyboardShortcuts = {}
if currentPlatform == "Darwin":
    #print("macOS")
    currentPlatform = "macOS"
    keyboardShortcuts = {
        'copy':[keyboard.Key.cmd, 'c'],
        'paste': [keyboard.Key.cmd, 'v'],
        'refresh':[keyboard.Key.cmd, 'r']
    }
elif currentPlatform == "Win32":
    #print("Windows")
    currentPlatform = "windows"
    keyboardShortcuts = {
        'copy':[keyboard.Key.ctrl, 'c'],
        'paste': [keyboard.Key.ctrl, 'v'],
        'refresh':[keyboard.Key.ctrl, 'r']
    }
elif currentPlatform == "Linux" or currentPlatform == "Linux2":
    #print("Linux")
    currentPlatform = "linux"
    keyboardShortcuts = {
        'copy':[keyboard.Key.ctrl, 'c'],
        'paste': [keyboard.Key.ctrl, 'v'],
        'refresh':[keyboard.Key.ctrl, 'r']
    }

#bbox = (0, 0, screen_width, screen_height)
currentCopy = ''
currentuser = getpass.getuser()
print(currentuser)
activePressedKeys = list()

df = pd.DataFrame({'Keys': [], 'Type': [], 'Note': [], 'Media': [], 'Platform':[], 'User':[]})

def onPress(key):

    try:
        #print('alphanumeric key {0} pressed'.format(key.char))
        activePressedKeys.append(key.char)
    except AttributeError:
        #print('special key {0} pressed'.format(key))
        activePressedKeys.append(key)

    newLog = {'Keys': activePressedKeys, 'Type': 'Alphanumeric', 'Note':'', 'Media': '', 'Platform': currentPlatform, 'User': currentuser}
    if (keyboard.Key.cmd in activePressedKeys) | (keyboard.Key.alt in activePressedKeys) | (keyboard.Key.ctrl in activePressedKeys):
        for shortcut, shortcutKeys in keyboardShortcuts.items():
        #print(shortcut + ': ' + str(shortcutKeys) + ' <> ' + str(activePressedKeys))
            if  activePressedKeys == shortcutKeys:
                newLog['Type'] = 'Shortcut'
                if shortcut == 'copy':
                    print('copy detected')
                    global currentCopy 
                    currentCopy = datetime.now().strftime("%H:%M:%S")
                    im = ImageGrab.grab(None)
                    im.save('copy - '+currentCopy+' - screenshot.png')
                    im.close()
                    newLog['Keys']="cmd + c"
                    newLog['Note'] = 'Copy Command'
                    newLog['Media'] = 'copy - '+currentCopy+' - screenshot.png'
                elif shortcut == 'paste':
                    print('paste detected')
                    im = ImageGrab.grab(None)
                    im.save('paste - ' + datetime.now().strftime("%H:%M:%S") +' from copy - '+currentCopy+' - screenshot.png')
                    im.close()
                    newLog['Keys']="cmd + v"
                    newLog['Note'] = 'Paste Command'
                    newLog['Media'] = 'paste - ' + datetime.now().strftime("%H:%M:%S") +' from copy - '+currentCopy+' - screenshot.png'
        #print(activePressedKeys)
    
    #else:
        #print(key)

    global df
    #print('OG')
    #print(df)
    # Need to add check for non alphanumerics
    if newLog['Type']== 'Shortcut':
        temp = pd.DataFrame(newLog, index=[0])
        
        df = pd.concat([df,temp])
    else:    
        df = pd.concat([df,pd.DataFrame.from_dict(newLog)])
    #print('Combined')
    #print(df)
    #If dataframe has more than 30 items write to file
    if len(df.index) >30:
        writeFile()
    #print(df)


def writeFile():
    global df
    df.to_csv(datetime.now().strftime("%Y-%m-%d") + '-log.csv', mode='a', index=False, header=False) 
    print('Data Written to Log')
    resetStoredKeys()           
    #clear out dataframe

def resetStoredKeys():
    global df
    df = pd.DataFrame({'Keys': [], 'Type': [], 'Note': [], 'Media': [], 'Platform':[], 'User':[]})
            
def onRelease(key):
    try:
        activePressedKeys.remove(key.char)
    except AttributeError:
        activePressedKeys.remove(key)
    #cactivePressedKeys.remove(key)
    #print('{0} released'.format(key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False
    #If dataframe has more than 10 items write to file

# Collect events until released
with keyboard.Listener(on_press=onPress, on_release=onRelease) as listener:
    listener.join()


