import time
import tkinter as tk

from pynput.keyboard import Listener

from UltraSockets import Client

c = None
pc = None


def start_client(host):
    global c, pc
    pc = Client(host, 'client')
    time.sleep(1)
    c = pc.get('all')[0][1]


def stop_client():
    pc.close()


root = tk.Tk()
canvas = tk.Canvas(root, width=480, height=240)
canvas.pack()

lHostHint = tk.Label(root, text='Host:')
lHostHint.place(relwidth=0.1, height=32)

tHost = tk.Text(root, padx=5, pady=8)
tHost.place(relwidth=0.9, height=32, relx=0.1)

client_btn_txt = tk.StringVar()
client_btn_txt.set('Connect')
btStartClient = tk.Button(root, textvariable=client_btn_txt)
btStartClient.place(height=32, y=32, relwidth=0.8, relx=0.1)

char_txt = tk.StringVar()
char_txt.set('Character string: ')
lCharString = tk.Label(root, textvariable=char_txt, padx=8)
lCharString.place(height=32, y=64)

root.mainloop()

print("Connection established")
print('You can use the following characters:', c)
print('This is your character string\n')
print('If you want to rebind these keys to other keys, then enter the rebind string')
print('It must be the same length as the character string, and include which key to replace it with, respectively')
print('For example , if your character string is abcd and you enter wasd, then w will press a on the server, '
      'a will press b, etc')

rebinds = None
while True:
    r = input('Rebind string: ')
    if not r:
        break
    elif not len(r) == len(c):
        print('Invalid rebind string!')
        continue

    rebinds = [rebind for rebind in r]
    break

chars = [char for char in c]
if rebinds is None:
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
