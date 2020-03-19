import subprocess

obj = subprocess.Popen(['ngrok', 'tcp', '8080'], shell=True, stdout=subprocess.PIPE)
output = obj.communicate()
print(str(output))
