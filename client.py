from pynput.keyboard import Key, Listener
import time
from UltraSockets import Client


print("The server should have printed the hostname")
host = input("Enter the hostname: ")
port = 8080
name = 'client'

pc = Client(host, port, name)
time.sleep(1)

c = pc.get('all')[0][1]

print("Connection established")
print('You can use the following characters:', c)

chars = [char for char in c]

pressedChars = []
for char in chars:
    pressedChars.append([char, False])


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
