from UltraSockets import Server
import pyautogui

host = '192.168.137.1'
port = 8080
server = Server(host,port,1,"server")
server.send("client","hi")

while True:
    data = server.get('all')
    if data:
        for objects in data:
            obj = objects[1]
            if obj[1] == 'n':
                pyautogui.keyUp(obj[0]);
            else:
                pyautogui.keyDown(obj[0]);
    
