from pynput import keyboard

activePressedKeys = list()
keyboardShortcuts = {
    'copy':[keyboard.Key.cmd, 'c'],
    #'cmd': [keyboard.Key.cmd],
    #'c keyc': ['c']
    'paste': [keyboard.Key.cmd, 'v']
}

def onPress(key):

    try:
        #print('alphanumeric key {0} pressed'.format(key.char))
        activePressedKeys.append(key.char)
    except AttributeError:
        #print('special key {0} pressed'.format(key))
        activePressedKeys.append(key)
    #print(activePressedKeys)
    for shortcut, shortcutKeys in keyboardShortcuts.items():
        #print(shortcut + ': ' + str(shortcutKeys) + ' <> ' + str(activePressedKeys))
        if  activePressedKeys == shortcutKeys:
            if shortcut == 'copy':
                print('copy detected')
            elif shortcut == 'paste':
                print('paste detected')            
        #else:
        #    print('')    
        
            
def onRelease(key):
    try:
        activePressedKeys.remove(key.char)
    except AttributeError:
        activePressedKeys.remove(key)
    #cactivePressedKeys.remove(key)
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False

# Collect events until released
with keyboard.Listener(on_press=onPress, on_release=onRelease) as listener:
    listener.join()