import time
import tkinter as tk

from pynput.keyboard import Listener

from UltraSockets import Client

c = None
pc = None
connected = False
rebinds = None
chars = None
pressedChars = None
listener = None


def on_press(k):
    global pressedChars, pc
    key = str(k).replace("'", "")
    if key in rebinds and not pressedChars[rebinds.index(key)][1]:
        pc.send("server", chars[rebinds.index(key)] + "y")
        pressedChars[rebinds.index(key)][1] = True


def on_release(k):
    global pressedChars, pc
    key = str(k).replace("'", "")
    if key in rebinds:
        pc.send("server", chars[rebinds.index(key)] + "n")
        pressedChars[rebinds.index(key)][1] = False


def start_client(host):
    global c, pc, char_txt, client_btn_txt, connected, chars, rebinds, pressedChars, listener
    try:
        pc = Client(host, 'client')
    except TypeError:
        connected = False
        return
    except ConnectionRefusedError:
        connected = False
        return
    client_btn_txt.set('Disconnect')
    time.sleep(1)
    c = pc.get('all')[0][1]

    char_txt.set('Character string: ' + c)

    chars = [char for char in c]
    rebinds = chars

    pressedChars = []
    for char in rebinds:
        pressedChars.append([char, False])

    listener = Listener(on_press=on_press, on_release=on_release)
    listener.start()


def stop_client():
    global client_btn_txt, listener
    pc.close()
    client_btn_txt.set('Connect')
    char_txt.set('Character string: ')
    listener.stop()


def toggle_client():
    global connected, tHost
    connected = not connected
    if connected:
        start_client(tHost.get('1.0', 'end-1c'))
    else:
        stop_client()


def update_rebinds():
    global rebinds, tRebinds, c, chars, pc, pressedChars
    pc.send('server', 'release_all')
    r = tRebinds.get('1.0', 'end-1c')
    if (not r) or not (len(r) == len(c)):
        print('Invalid rebind string!')
        rebinds = chars
    else:
        rebinds = [rebind for rebind in r]

    pressedChars = []
    for char in rebinds:
        pressedChars.append([char, False])


root = tk.Tk()
root.title('GamingOverLAN Client')
canvas = tk.Canvas(root, width=480, height=180)
canvas.pack()

lHostHint = tk.Label(root, text='Host:')
lHostHint.place(relwidth=0.1, height=32)

tHost = tk.Text(root, padx=5, pady=8)
tHost.place(relwidth=0.9, height=32, relx=0.1)

client_btn_txt = tk.StringVar()
client_btn_txt.set('Connect')
btStartClient = tk.Button(root, textvariable=client_btn_txt, command=toggle_client)
btStartClient.place(height=32, y=32, relwidth=0.8, relx=0.1)

char_txt = tk.StringVar()
char_txt.set('Character string: ')
lCharString = tk.Label(root, textvariable=char_txt, padx=8)
lCharString.place(height=32, y=64)

lRebinds = tk.Label(root, text='Rebind string: ')
lRebinds.place(relwidth=0.2, y=96, height=32)

tRebinds = tk.Text(root, padx=5, pady=8)
tRebinds.place(relwidth=0.75, relx=0.2, height=32, y=96)

btUpdateRebinds = tk.Button(root, text='Update rebinds', command=update_rebinds)
btUpdateRebinds.place(relwidth=0.8, height=32, y=140, relx=0.1)

root.mainloop()
