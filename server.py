import socket
import tkinter as tk
from threading import Thread

import pyautogui

from UltraSockets import Server


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0] + ':8080'


running = False
thread = None
server = None
host_ip = get_ip_address()


def run_server(host, chars):
    print("Starting server...")
    global server, running
    server = Server(host, 1, 'server')
    server.send('client', chars)
    print("Server running...")
    while running:
        data = server.get('all')
        if data:
            for objects in data:
                obj = objects[1]
                if obj[1] == 'n':
                    pyautogui.keyUp(obj[0])
                else:
                    pyautogui.keyDown(obj[0])

    server = None


def toggle_host():
    global tSelectHost, tSelectChar, running, thread, host_ip
    print("Button pressed")
    running = not running
    print('Running:', running)
    if running:
        host = tSelectHost.get('1.0', 'end-1c')
        if not host:
            host = host_ip
        chars = tSelectChar.get('1.0', 'end-1c')
        thread = Thread(target=run_server, args=[host, chars])
        thread.start()
    else:
        thread.join()


root = tk.Tk()
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

btServerToggle = tk.Button(root, text='Start Host', padx=10, pady=5, command=toggle_host)
btServerToggle.place(height=32, y=144, relwidth=0.2, relx=0.4)

root.mainloop()
