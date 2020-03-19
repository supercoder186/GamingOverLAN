import tkinter as tk

from pyngrok import ngrok


def set_token():
    global tAuthToken, success_txt
    auth_token = tAuthToken.get('1.0', 'end-1c')
    ngrok.set_auth_token(auth_token)
    success_txt.set('Token set to ' + auth_token)


root = tk.Tk()
root.title('Ngrok Setup')
canvas = tk.Canvas(root, width=480, height=120)
canvas.pack()

lAuthToken = tk.Label(root, text='Auth token:')
lAuthToken.place(relwidth=0.2, height=32)

tAuthToken = tk.Text(root)
tAuthToken.place(relwidth=0.7, height=32, relx=0.25)

btAuthSubmit = tk.Button(root, text="Set Auth Token", command=set_token)
btAuthSubmit.place(relwidth=0.8, height=32, y=40, relx=0.1)

success_txt = tk.StringVar()
lSuccess = tk.Label(root, textvariable=success_txt)
lSuccess.place(relwidth=1, height=32, y=80)

root.mainloop()
