import time
import tkinter as tk

from pynput.keyboard import Listener

from UltraSockets import Client

# declare and assign all global variables
c = None
pc = None
connected = False
rebinds = None
chars = None
pressedChars = None
listener = None


# define the functions for when a button is pressed or released
def on_press(k):
    global pressedChars, pc
    key = str(k).replace("'", "")  # remove the surrounding quotes
    # checks if the pressed key is in the allowed character list, taking rebinds into account
    if key in rebinds and not pressedChars[rebinds.index(key)][1]:
        pc.send("server", chars[rebinds.index(key)] + "y")  # tell server that key has been pressed
        pressedChars[rebinds.index(key)][1] = True  # store that the key has been pressed


def on_release(k):
    global pressedChars, pc
    key = str(k).replace("'", "")  # remove the surrounding quotes
    # checks if the pressed key is in the allowed character list, taking rebinds into account
    if key in rebinds:
        pc.send("server", chars[rebinds.index(key)] + "n")  # tell server that key has been released
        pressedChars[rebinds.index(key)][1] = False  # store that the key has been released


def start_client(host):
    global c, pc, char_txt, client_btn_txt, connected, chars, rebinds, pressedChars, listener
    try:
        pc = Client(host, 'client')  # start client and connect to host
    except TypeError as e:
        # this is raised if the format of the host is incorrect. Use the format <ip>:<port>
        connected = False
        return
    except ConnectionRefusedError as e:
        print(e)
        connected = False  # if connection is refused, set connected to False
        return
    client_btn_txt.set('Disconnect')  # change text on button

    # wait until the server sends the character list
    obj = None
    while obj is None:
        time.sleep(0.1)
        obj = pc.get('all')

    c = obj[0][1]  # retrieves the character list from the sent data

    char_txt.set('Character string: ' + c)

    chars = [char for char in c]  # turns the character string into a list
    rebinds = chars

    pressedChars = []
    for char in rebinds:
        pressedChars.append([char, False])  # creates the list of pressed characters. All are False in the beginning

    listener = Listener(on_press=on_press, on_release=on_release)  # define the key press listener
    listener.start()  # start the key press listener


def stop_client():
    global client_btn_txt, listener
    pc.close()  # notify the server that the client is leaving
    client_btn_txt.set('Connect')  # change the client button text
    char_txt.set('Character string: ')  # change the character string display text
    listener.stop()  # stop the key listener


def toggle_client():
    global connected, tHost
    connected = not connected  # toggle connected
    if connected:  # check if the client has an active connection
        start_client(tHost.get('1.0', 'end-1c'))  # start the client
    else:
        stop_client()  # stop the client


def update_rebinds():
    global rebinds, tRebinds, c, chars, pc, pressedChars
    pc.send('server', 'release_all')  # tell the server to release all keys
    r = tRebinds.get('1.0', 'end-1c')  # retrieve the rebind string from the text field
    if (not r) or not (len(r) == len(c)):  # checks if the rebind string is the right length
        print('Invalid rebind string!')
        rebinds = chars  # disable rebinds by setting all rebinds to their respective characters
    else:
        rebinds = [rebind for rebind in r]  # change the rebind list

    # reassign pressedChars based on the new rebind string
    pressedChars = []
    for char in rebinds:
        pressedChars.append([char, False])


# Define the layout
root = tk.Tk()
root.title('GamingOverLAN Client')
canvas = tk.Canvas(root, width=480, height=200)
canvas.pack()

lHostHint = tk.Label(root, text='Host:')
lHostHint.place(relwidth=0.1, height=32)

tHost = tk.Text(root, padx=5, pady=8)
tHost.place(relwidth=0.9, height=32, relx=0.1)

client_btn_txt = tk.StringVar(value='Connect')
btStartClient = tk.Button(root, textvariable=client_btn_txt, command=toggle_client)
btStartClient.place(height=32, y=40, relwidth=0.8, relx=0.1)

char_txt = tk.StringVar(value='Character string: ')
lCharString = tk.Label(root, textvariable=char_txt, padx=8)
lCharString.place(height=32, y=80)

lRebinds = tk.Label(root, text='Rebind string: ')
lRebinds.place(relwidth=0.2, y=120, height=32)

tRebinds = tk.Text(root, padx=5, pady=8)
tRebinds.place(relwidth=0.75, relx=0.2, height=32, y=120)

btUpdateRebinds = tk.Button(root, text='Update rebinds', command=update_rebinds)
btUpdateRebinds.place(relwidth=0.8, height=32, y=160, relx=0.1)

# Start the UI loop
root.mainloop()
