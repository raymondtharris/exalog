from pynput import keyboard
from PIL import ImageGrab
from datetime import datetime
from pathlib import Path
import pandas as pd

#bbox = (0, 0, screen_width, screen_height)
currentCopy = ''
activePressedKeys = list()
keyboardShortcuts = {
    'copy':[keyboard.Key.cmd, 'c'],
    #'cmd': [keyboard.Key.cmd],
    #'c keyc': ['c']
    'paste': [keyboard.Key.cmd, 'v']
}
df = pd.DataFrame({'Keys': [], 'Type': [], 'Note': [], 'Media': []})

def onPress(key):

    try:
        #print('alphanumeric key {0} pressed'.format(key.char))
        activePressedKeys.append(key.char)
    except AttributeError:
        #print('special key {0} pressed'.format(key))
        activePressedKeys.append(key)

    newLog = {'Keys': activePressedKeys, 'Type': 'Alphanumeric', 'Note':'', 'Media': ''}
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
        print(activePressedKeys)
    
    else:
        print(key)
    global df    
    df = pd.concat([df,pd.DataFrame([newLog])], join='inner', ignore_index=True)
    #If dataframe has more than 30 items write to file
    if len(df.index) >30:
        writeFile()
    #print(df)


def writeFile():
    df.to_csv(datetime.now().strftime("%Y-%m-%d") + '-log.csv', mode='a', index=False, header=False) 
    resetStoredKeys()           
    #clear out dataframe

def resetStoredKeys():
    global df
    df = pd.DataFrame({'Keys': [], 'Type': [], 'Note': [], 'Media': []})
            
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


