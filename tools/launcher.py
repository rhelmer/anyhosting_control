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


class Server():
    def __init__(self):
        config = ConfigParser.ConfigParser()
        config.read('launcher.cfg')
        rimu_api_key = config.get('Main','RIMU_API_KEY')
        self.master_image = config.get('Main','MASTER_IMAGE')
        self.server_size = config.get('Main','SERVER_SIZE')
        self.domain = config.get('Main','DOMAIN')

        self.hostname = socket.gethostname()

        self.cloud = RimuHostingNodeDriver(rimu_api_key)
        self.all_nodes = self.cloud.list_nodes()

    def checkChildren(self):
        for child_hostname in [self.hostname+'A', self.hostname+'B']:
            child_instance_id = None
            child_fqdn = '%s.%s' % (child_hostname, self.domain)
            try:
                child_instance_id = self.getInstanceId(child_fqdn)
                self.monitor(child_fqdn)
            except Exception,e:
                print "%s not responding to monitor, restarting. Exception: %s" % (child_fqdn, e)
                try:
                    if child_instance_id != None: 
                        self.destroy(child_instance_id)
                    node = self.create(child_fqdn, self.master_image, self.server_size)
                    reportDNS(child_fqdn, node.ipaddress)
                except Exception,ex:
                    self.sendNotification(child_fqdn, ex)
                    raise ex

    def getInstanceId(self, hostname):
        # return the first server that has this hostname
        for node in self.all_nodes:
            if hostname == node.name:
                return node.id
            else:
                return None

    def sendNotification(self, hostname, e):
        print "Need human attention, unable to restart %s. Exception: %s" % (hostname, e)

    """
    A monitors B and C; if these are not passing monitoring tests then the
    server instances are terminated and they are restarted. The root node
    ("A") is externally monitored and restarted, manually if necessary.

    """
    def monitor(self, hostname):
        # TODO
        raise Exception('Monitoring failed for %s' % hostname)

    def create(self, hostname, master_image, server_size):
        # TODO
        #self.cloud.create_node(name=hostname, image=master_image, size=server_size)
        raise Exception('Could not create %s' % hostname)

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
    def sync(self):
        # TODO
        # $ rsync -a rsync://admin/anyhosting/etc/apache2/ /etc/apache2/
        # $ rsync -a rsync://admin/anyhosting/www/ /var/www/
        raise Exception('Could not sync %s' % self.hostname)

    """
    DNS servers are external to this system. Nodes are responsible for reporting
    themselves to the DNS server.
    """
    def reportDNS(self, hostname, ipaddress):
        # TODO https://rimuhosting.com/dns/dyndns.jsp
        raise Exception('Could not sync %s' % self.hostname)

def main(argv):
    server = Server()
    try:
        server.sync()
    except Exception,e:
        print e

    try:
        server.checkChildren()
    except Exception,e:
        print e

if __name__ == '__main__':
    sys.exit(main(sys.argv))
