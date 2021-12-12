import subprocess
network = subprocess.check_output(['netsh', 'wlan', 'show','profiles']).decode('utf-8').split('\n')
 
profiles = [i.split(":")[1][1:-1] for i in network if "All User Profile" in i]
 
for i in profiles:
    results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i,'key=clear']).decode('utf-8').split('\n')
    results = [net.split(":")[1][1:-1] for net in results if "Key Content" in net]
    print ("{:<30}|  {:<}".format(i, results[0]))