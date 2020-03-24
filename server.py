import os
import socket
import time
import tkinter as tk
from threading import Thread

import pyautogui
from pyngrok import ngrok
from pyngrok.exception import PyngrokNgrokError

from UltraSockets import Server


def get_ip_address():
    # This function opens a temporary socket that is used to find the computer's ip
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0] + ':8080'


ngrok.kill()  # kills any running ngrok processes
# declare and assign all global variables
running = False
thread = None
server = None
host_ip = get_ip_address()  # assigns host ip to the PC's IP address on the network
chars = None
host = None
region_names = ['India', 'United States', 'Europe', 'Asia/Pacific', 'Australia', 'South America', 'Japan']
regions = ['in', 'us', 'eu', 'ap', 'au', 'sa', 'jp']
region = regions[0]


def run_server(server_host, characters):
    global server
    # starts the server, and start waiting for client connections
    server = Server(server_host, 1, 'server')
    time.sleep(0.5)  # Wait for 0.5 seconds to ensure the handshake is completed - allows for higher ping connections
    server.send('client', characters)  # The server sends the client the allowed characters
    while True:
        # The server retrieves any data that it has received
        data = server.get('all')
        if data:
            for objects in data:
                obj = objects[1]
                # The server then performs the corresponding action on the key
                if obj == 'release_all':
                    # If the message is to release all keys, this is done
                    for char in characters:
                        pyautogui.keyUp(char)
                else:
                    # The server checks if the message is to release the key or press it
                    if obj[1] == 'n':
                        pyautogui.keyUp(obj[0])
                    else:
                        print('Pressing key:', obj[0])
                        pyautogui.keyDown(obj[0])


def set_region(rgn):
    global region
    region = rgn


def toggle_host():
    global tSelectHost, tSelectChar, running, thread, host_ip, btn_text, chars, client_host_text, host, useNgrok
    global region

    # running is toggled
    running = not running
    if running:
        chars = tSelectChar.get('1.0', 'end-1c')  # Load the allowed characters from the text field
        if useNgrok.get():  # checks if the user enabled use ngrok
            rgn = regions[region_names.index(region.get())]  # gets the region name
            set_region(rgn)  # sets the region
            try:
                host = ngrok.connect(8080, proto='tcp', region=region)  # start the ngrok tunnel
            except PyngrokNgrokError:  # check if ngrok failed to start
                print('Ngrok failed!')
                # kill the ngrok process and exit the program with an error code
                ngrok.kill()
                os._exit(1)
            # create the run server thread
            thread = Thread(target=run_server, args=['localhost:8080', chars])
        else:
            # data is retrieved from both text fields
            host = tSelectHost.get('1.0', 'end-1c')
            if not host:
                # If the host is left empty, it is replaced with auto-detected host
                host = host_ip
            # create the run server thread
            thread = Thread(target=run_server, args=[host, chars])
        thread.start()  # start the server thread
        btn_text.set('Stop Server')  # change the button text
        client_host_text.set('Hostname for Client: ' + host)  # display the client host so it is copiable
    else:
        # when Stop Server is pressed, the application is terminated
        ngrok.kill()
        os._exit(0)


def copy_host():  # copy the host when the button is pressed
    global root
    root.clipboard_clear()
    root.clipboard_append(host)


# define the layout
root = tk.Tk()
root.title('GamingOverLAN Server')
canvas = tk.Canvas(root, width=480, height=320)
canvas.pack()

lAutoDetect = tk.Label(root, text='The auto-detected hostname is: ' + get_ip_address())
lAutoDetect.place(height=32, relwidth=1)

lHostHint = tk.Label(root, text='Hostname (Leave blank for auto-detected)')
lHostHint.place(height=32, relwidth=1, y=40)

tSelectHost = tk.Text(root, padx=5, pady=4)
tSelectHost.place(height=32, y=80, relwidth=0.9, relx=0.05)

useNgrok = tk.BooleanVar()
cbUseNgrok = tk.Checkbutton(root, variable=useNgrok)
cbUseNgrok.place(height=32, y=120, relwidth=0.1, relx=0.05)

lUseNgrok = tk.Label(root, text='Use ngrok (overrides hostname)')
lUseNgrok.place(height=32, y=120, relx=0.15)

lRegion = tk.Label(root, text='Ngrok region: ')
lRegion.place(height=32, y=160, relwidth=0.2, relx=0.025)

region = tk.StringVar(value=region_names[0])
omRegion = tk.OptionMenu(root, region, *region_names)
omRegion.place(height=32, y=160, relwidth=0.7, relx=0.25)

lCharHint = tk.Label(root, text='Characters:')
lCharHint.place(height=32, relwidth=0.2, y=200)

tSelectChar = tk.Text(root, padx=5, pady=4)
tSelectChar.place(height=32, y=200, relwidth=0.7, relx=0.25)

client_host_text = tk.StringVar(value='Hostname for Client: ')
lClientHost = tk.Label(root, textvariable=client_host_text)
lClientHost.place(height=32, y=240, relwidth=0.7, relx=0.05)

btHostCopy = tk.Button(root, text='Copy', command=copy_host)
btHostCopy.place(height=32, y=240, relwidth=0.2, relx=0.8)

btn_text = tk.StringVar(value='Start Server')
btServerToggle = tk.Button(root, textvariable=btn_text, padx=10, pady=5, command=toggle_host)
btServerToggle.place(height=32, y=280, relwidth=0.2, relx=0.4)

# start the UI thread
root.mainloop()

# when the UI is closed, terminate the application
ngrok.kill()  # kill ngrok
os._exit(0)  # kill the program
