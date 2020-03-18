import socket
import tkinter as tk

import pyautogui

from UltraSockets import Server


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0] + ':8080'


host_ip = get_ip_address()

root = tk.Tk()
canvas = tk.Canvas(root, width=640, height=480)
canvas.pack()

autoHostDetect = tk.Label(root, text='The auto-detected hostname is: ' + get_ip_address())
autoHostDetect.place(height=32, relwidth=1)

hostHint = tk.Label(root, text='Hostname (Leave blank for auto-detected)')
hostHint.place(height=32, relwidth=1, y=32)

selectHost = tk.Text(root, padx=5, pady=4)
selectHost.place(height=32, y=64, relwidth=0.9, relx=0.05)

root.mainloop()

print("Enter what keys the client should be able to use eg. wasd")
chars = "".join(set(input('Characters: ')))

print('Enter the hostname you want to use\nLeave the field blank to use the provided hostname')
host = input('Hostname: ')
if not host:
    host = host_ip

print('Using', host, 'as host')
server = Server(host, 1, "server")
server.send("client", chars)

while True:
    data = server.get('all')
    if data:
        for objects in data:
            obj = objects[1]
            if obj[1] == 'n':
                pyautogui.keyUp(obj[0])
            else:
                pyautogui.keyDown(obj[0])
