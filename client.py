from pynput.keyboard import Key, Listener
import time
from UltraSockets import Client

host = '192.168.137.1'
port = 8080
name = 'client'

pc = Client(host, port, name)
time.sleep(1)

print(pc.get('all')[0][1])
print("Connection established")

chars = [char for char in 'qesdf']

pressedChars = []
for char in chars:
    pressedChars.append([char, False])

print(pressedChars)

def on_press(k):
    key = str(k).replace("'", "")
    if key in chars and not pressedChars[chars.index(key)][1]:
        pc.send("server", key + "y")
        pressedChars[chars.index(key)][1] = True


def on_release(k):
    key = str(k).replace("'", "")
    if key in chars:
        pc.send("server", key + "n")      
        pressedChars[chars.index(key)][1] = False


with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
