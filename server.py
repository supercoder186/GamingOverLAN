import os
import socket
import tkinter as tk
from threading import Thread

import pyautogui

from UltraSockets import Server


def get_ip_address():
    # This function opens a temporary socket that is used to find the computer's ip
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0] + ':8080'


running = False
thread = None
server = None
host_ip = get_ip_address()
chars = None


def run_server(host, characters):
    global server
    # This starts the server, and the server begins waiting for client connections
    server = Server(host, 1, 'server')
    # The server sends the client the allowed characters
    server.send('client', characters)
    while True:
        # The server retrieves any data that it has received
        data = server.get('all')
        if data:
            for objects in data:
                obj = objects[1]
                # The server then performs the corresponding action on the key
                if obj == 'release_all':
                    for char in characters:
                        pyautogui.keyUp(char)
                else:
                    if obj[1] == 'n':
                        pyautogui.keyUp(obj[0])
                    else:
                        print('Pressing key:', obj[0])
                        pyautogui.keyDown(obj[0])


def toggle_host():
    global tSelectHost, tSelectChar, running, thread, host_ip, btn_text, chars
    running = not running
    if running:
        # Data is retrieved from both text fields
        host = tSelectHost.get('1.0', 'end-1c')
        if not host:
            # If the host is left empty, it is replaced with auto-detected host
            host = host_ip
        chars = tSelectChar.get('1.0', 'end-1c')
        # Starts new server thread
        thread = Thread(target=run_server, args=[host, chars])
        thread.start()
        btn_text.set('Stop Server')
    else:
        # noinspection PyProtectedMember
        # When Stop Server is pressed, the application is terminated
        os._exit(0)


# Defining the layout
root = tk.Tk()
root.title('GamingOverLAN Server')
canvas = tk.Canvas(root, width=480, height=180)
canvas.pack()

autoHostDetect = tk.Label(root, text='The auto-detected hostname is: ' + get_ip_address())
autoHostDetect.place(height=32, relwidth=1)

lHostHint = tk.Label(root, text='Hostname (Leave blank for auto-detected)')
lHostHint.place(height=32, relwidth=1, y=32)

tSelectHost = tk.Text(root, padx=5, pady=4)
tSelectHost.place(height=32, y=64, relwidth=0.9, relx=0.05)

lCharHint = tk.Label(root, text='Characters:')
lCharHint.place(height=32, relwidth=0.2, y=104)

tSelectChar = tk.Text(root, padx=5, pady=4)
tSelectChar.place(height=32, y=104, relwidth=0.7, relx=0.25)

btn_text = tk.StringVar(value='Start Server')
btServerToggle = tk.Button(root, textvariable=btn_text, padx=10, pady=5, command=toggle_host)
btServerToggle.place(height=32, y=144, relwidth=0.2, relx=0.4)

root.mainloop()
