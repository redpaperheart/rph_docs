'''
This script allows you to power on and off a defined list of LG displays over a network.
example: `python lg_control.py on` will attempt to turn on all of the displays in the tvClients list

install python 3+

install wakeonlan
pip install wakeonlan

install pywebostv
pip install pywebostv
More examples here: https://github.com/supersaiyanmode/PyWebOSTV

Enable wake on LAN on tvs
- hold down settings button for 5 seconds
- when little word balloon comes up press-> 0 0 0 0 OK
- a admin menu should come up with the options

Note the IP address of each display or configure displays to have static IPs

options
- reg: register with tv
- disc: discover? (not implemented)
- on: turn tv on
- off: turn tv off

example:
`python lg_control.py reg`

start by registering all the tvs
this will return an ip and client key for each tv
add them to the tvClients list
also add the mac address, this is needed for wakeonlan 
'''

import sys

from pywebostv.discovery import *
from pywebostv.connection import *
from pywebostv.controls import *

from wakeonlan import send_magic_packet

#Clients
#client_keys should be empty until televisions have been registered.
#once registered use the client key sent from the display during the registration process
tvClients = [{'ip': '10.140.60.38', 'client_key': 'c384088a59d439a5e56a0e7fc1a175ec', 'mac': '78.5D.C8.9A.73.93'},
             {'ip': '10.140.60.39', 'client_key': '6f9c817099edd2e7c2a2e5fd9bbe6846', 'mac': '78.5D.C8.9A.73.68'},
             {'ip': '10.140.60.40', 'client_key': '67725b1ba08239d519b9959499caad81', 'mac': '78.5D.C8.92.1D.07'}
]

def register(tvID):
    global tvClients
    clientTV = WebOSClient(tvClients[tvID]['ip'])
    clientTV.connect()
    result = {'client_key': tvClients[tvID]['client_key']}
    for status in clientTV.register(result):
        if status == WebOSClient.PROMPTED:
            print("Please accept the connection on the TV!")
        elif status == WebOSClient.REGISTERED:
            #make sure we're registered
            print('Registered Client Key! Add to tvClients list\n', tvClients[tvID]['ip'], result)
    return

def turnOff(tvID):
    global tvClients
    print('turning off: ' + str(tvClients[tvID]['ip']))
    try:
        clientTV = WebOSClient(tvClients[tvID]['ip'])
        clientTV.connect()
        #make sure we're registered
        result = {'client_key': tvClients[tvID]['client_key']}
        for status in clientTV.register(result):
            if status == WebOSClient.PROMPTED:
                print("Please accept the connect on the TV!")
            elif status == WebOSClient.REGISTERED:
                print("Registered: ", result)
        system = SystemControl(clientTV)
        system.power_off()
    except TimeoutError:
        print('TimeoutError: connection with tv timed out')


def turnOn(tvID):
    global tvClients
    #send the wakeonlan magic packet multiple (5) times to ensure it arrives
    for l in range(0, 5):
        print('turning on: ' + str(tvClients[tvID]['ip']))
        send_magic_packet(str(tvClients[tvID]['mac']))

if(len(sys.argv)<2):
    # print('please supply an argument: reg | on | off')
    print('please supply an argument: reg | on | off')
else:
    command = str(sys.argv[1])
    #loop through all clients
    for i, val in enumerate(tvClients):
        if(command == 'reg'):
            register(i)
        elif(command == 'on'):
            turnOn(i)
        elif(command == 'off'):
            turnOff(i)
        else:
            print('unknown command ', command)
