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

import sys
import socket
import ConfigParser
# FIXME support other providers
#from libcloud.types import Provider
#from libcloud.providers import get_driver
from libcloud.drivers.rimuhosting import RimuHostingNodeDriver

config = ConfigParser.ConfigParser()
config.read('launcher.cfg')
RIMU_API_KEY = config.get('Main','RIMU_API_KEY')
MASTER_IMAGE = config.get('Main','MASTER_IMAGE')
SERVER_SIZE = config.get('Main','SERVER_SIZE')

class Server():
    def __init__(self):

        self.hostname = socket.gethostname()
        # this assumes that /etc/hosts is set correctly, and not to 127.0.0.1
        self.ipaddress = socket.gethostbyname(self.hostname)
        self.cloud = RimuHostingNodeDriver(RIMU_API_KEY)
        self.all_nodes = self.cloud.list_nodes()

    def checkChildren(self):
        for child in [self.hostname+'A', self.hostname+'B']:
            child_hostname = self.hostname + child
            child_instance_id = None
            try:
                child_instance_id = self.getInstanceId(child_hostname)
                self.monitor(child_hostname)
            except Exception,e:
                print "%s not responding to monitor, restarting" % child_hostname
                try:
                    if child_instance_id != None: 
                        self.destroy(child_instance_id)
                    self.create(child_hostname)
                except Exception,ex:
                    self.sendNotification(child_hostname, ex)

    def getInstanceId(self, hostname):
        # return the first server that has this hostname
        return filter(lambda x: x.name==hostname, self.all_nodes)[0].id

    def sendNotification(self, child_hostname, notice):
        print "Need human attention, cannot manage %s. Exception: %s" % (child_hostname, notice)

    """
    A monitors B and C; if these are not passing monitoring tests then the
    server instances are terminated and they are restarted. The root node
    ("A") is externally monitored and restarted, manually if necessary.

    """
    def monitor(self, ipaddress):
        # TODO
        raise Exception('Monitoring failed for %s' % ipaddress)

    def create(self, child_hostname):
        # TODO
        #self.cloud.create_node(name=child_hostname, image=MASTER_IMAGE, size=SERVER_SIZE)
        raise Exception('Could not create %s' % child_hostname)

    def destroy(self, instance_id):
        # TODO
        #self.cloud.destroy_node(instance_id)
        raise Exception('Could not destroy %s' % instance_id)

    """
    Every server is an independent agent. The only difference between servers
    is their IP and MAC addresses; these are used (via a DNS lookup) to determine 
    which websites this server should serve. The content and config is pulled from 
    a central store.

    TODO: look into puppet
    """
    def serverSync(self):
        # TODO
        # $ rsync -a rsync://admin/anyhosting/etc/apache2/ /etc/apache2/
        # $ rsync -a rsync://admin/anyhosting/www/ /var/www/
        pass

    """
    DNS servers are external to this system. Nodes are responsible for reporting
    themselves to the DNS server.
    """
    def reportDNS(self):
        # TODO 
        pass

def main(argv):
    server = Server()
    server.serverSync()
    server.checkChildren()

if __name__ == '__main__':
    sys.exit(main(sys.argv))
