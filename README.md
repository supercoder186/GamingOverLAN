# GamingOverLAN
Allows the user to broadcast keyboard inputs from a client to server in order to play games over multiple PCs (and more)

## Dependency Installation
There is a requirements.txt included in the package, meaning that dependency installation can be done in one command.
Run this in the root folder of the package:
```sh
pip install -r requirements.txt
```
That's it! All the requirements are automatically installed by pip

## Setting up ngrok
Set up ngrok if you want to play over the internet when the Server and Client are connected to different networks. This
is mandatory if you want to use ngrok

### Creating an account
Go to the [ngrok website](https://github.com/user/repo/blob/branch/other_file.md) and sign up for an account

### Getting your auth token
After creating an ngrok account, go to the [auth dashboard](https://dashboard.ngrok.com/auth) and copy your Tunnel
Authtoken. 

### Setting your auth token
Open ngroksetup.py and paste this in the provided text field. Click the Set Auth Token button in order to
finalise the auth token and store it. If this is successful, a text field will appear showing you the auth token you
entered in order to confirm that the auth token has been set successfully

## Hosting the server
Use server.py to achieve this. The features are listed below:

### Auto-detection of hostname
The hostname is automatically detected by the code and is shown in the top of the window. If you wish to use
this as your host, leave the hostname field blank. The automatically detected hostname will be used as the host
and displayed in the hostname for client field so it can be copied and sent to the client PC. Note that you have
to be on the same wi-fi network in order for this to work. If you are not connected to the same router, then use ngrok
(detailed later)

### Using your own host
If you fill in a hostname, then this will be used unless you choose to use ngrok. This can be used in case the 
automatic host detection works incorrectly(unlikely) or if the laptops are connected by an ethernet cable to lower input
lag (recommended if you understand how IP addresses work)

### Using ngrok
Only use ngrok if it is impossible to connect to the same router as the other computer, since it introduces lag because
it sends the key presses via an external server (it's secure, don't worry)

#### Ngrok region
When choosing the ngrok region, ensure that you choose the region (geographically)closest to you in order to minimize
ping and therefore input lag

### Setting the usable characters
Enter the characters into the characters text field without any separation. Arrow keys and Space are not supported.
e.g. - 'wasd' or 'esdf' (without the quotes)

### Starting the server
In order to start the server, simply click start server after entering all the required fields

#### Required fields
Using auto-detected hostname: characters  
Using ngrok: ngrok checkbox, ngrok region, characters  
Using own hostname: hostname, characters

### Copying the hostname
Once the server has been started, click the Copy button in order to copy the hostname to give to the Client PC. This can
then be sent to the Client PC in order to connect to the server

