from UltraSockets import Server
import pyautogui
import socket


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


host_ip = get_ip_address()

print("Detected hostname is:", host_ip)

print("Enter what keys the client should be able to use eg. wasd")
chars = "".join(set(input('Characters: ')))

print('Enter the hostname you want to use\nLeave the field blank to use the provided hostname')
host = input('Hostname: ')
if not host:
    host = host_ip

print('Using', host, 'as host')
port = 8080
server = Server(host,port,1,"server")
print(chars)
server.send("client", chars)

while True:
    data = server.get('all')
    if data:
        for objects in data:
            obj = objects[1]
            if obj[1] == 'n':
                pyautogui.keyUp(obj[0]);
            else:
                pyautogui.keyDown(obj[0]);
