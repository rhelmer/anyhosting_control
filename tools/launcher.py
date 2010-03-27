#!/usr/bin/python
"""
AnyHosting scalable web service

This script should be started and maintained as a service by the default
install image.

Each server controls two servers:

           -----
           | A |
           -----
             |
           /   \
      -----     -----
      | B |     | C |
      -----     -----
      |             |
     / \           / \
-----   ----- -----   -----
| BB|   | BC| | CA|   | CB|
-----   ----- -----   -----
"""

import ping,socket

def checkChildren(self):
    for child in ['A', 'B']:
        hostname = self.hostname + 'child'
        instance_id = getInstanceId(hostname)
        try:
          monitor(hostname)
        except:
          sendNotification()
          stopServer(instance_id)
          startServer()

def getInstanceId(hostname):
    # TODO figure out how to get this from provider
    # libcloud?
    pass

def sendNotification():
    # TODO email
    pass

"""
A monitors B and C; if these are not passing monitoring tests then the
server instances are terminated and they are restarted. The root node
("A") is externally monitored and restarted, manually if necessary.

TODO: look into libcloud
"""
def monitor(hostA):
    delay = ping.do_one(ipaddress, timeout=2)

def startServer():
    pass

def stopServer(instance_id):
    pass

"""
Every server is an independent agent. The only difference between servers
is their IP and MAC addresses; these are used (via a DNS lookup) to determine 
which websites this server should serve. The content and config is pulled from 
the central git server.

The git repo is on all servers, but only A is written to (the others sync the repo from A). 

TODO: look into puppet
"""
def serverSync(self):
    # 1) always check master for changes
    #  $ git pull /var/svn/anyhosting /home/sys/anyhosting
    pass

"""
DNS servers are external to this system. Nodes are responsible for reporting
themselves to the DNS server.
"""
def reportDNS(self):
    pass

def main(argv):
    self.hostname = socket.gethostname()
    # this assumes that /etc/hosts is set correctly, and not to 127.0.0.1
    self.ipaddress = socket.gethostbyname(hostname)
    while True:
        self.checkChildren()
        self.serverSync()
