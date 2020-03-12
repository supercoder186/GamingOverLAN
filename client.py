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
print('This is your character string\n')
print('If you want to rebind these keys to other keys, then enter the rebind string')
print('It must be the same length as the character string, and include which key to replace it with, respectively')
print('For example , if your character string is abcd and you enter wasd, then w will press a on the server, a will press b, etc')

rebinds = None
while True:
    r = input('Rebind string: ')
    if not len(r) == len(c):
        print('Invalid rebind string!')
        continue
    
    rebinds = [rebind for rebind in r]
    break

chars = [char for char in c]
if rebinds == None:
    rebinds = chars

pressedChars = []
for char in rebinds:
    pressedChars.append([char, False])


def on_press(k):
    key = str(k).replace("'", "")
    if key in rebinds and not pressedChars[rebinds.index(key)][1]:
        pc.send("server", chars[rebinds.index(key)] + "y")
        pressedChars[rebinds.index(key)][1] = True


def on_release(k):
    key = str(k).replace("'", "")
    if key in rebinds:
        pc.send("server", chars[rebinds.index(key)] + "n")      
        pressedChars[rebinds.index(key)][1] = False


with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
