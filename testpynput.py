from pynput.keyboard import Key, Controller

keyboard = Controller()
keyboard.press('r')
keyboard.release('r')
