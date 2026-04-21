from pox.core import core
from pox.lib.revent import *
from pox.lib.util import dpidToStr
import pox.openflow.libopenflow_01 as of
from pox.lib.packet.ethernet import ethernet
from pox.lib.packet.arp import arp

log = core.getLogger()

class HostDiscovery(EventMixin):
    def __init__(self):
        self.hosts = {}
        core.openflow.addListeners(self)
        log.info("Host Discovery Service started")

    def _handle_PacketIn(self, event):
        packet = event.parsed
        if not packet.parsed:
            return

        mac = str(packet.src)
        dpid = dpidToStr(event.dpid)
        port = event.port

        ip = None
        arp_packet = packet.find('arp')
        if arp_packet:
            ip = str(arp_packet.protosrc)

        if mac not in self.hosts:
            log.info("New host detected -- MAC: %s IP: %s Switch: %s Port: %s", mac, ip, dpid, port)

        self.hosts[mac] = {
            'ip': ip if ip else self.hosts.get(mac, {}).get('ip', 'Unknown'),
            'dpid': dpid,
            'port': port
        }

        self.display_hosts()

    def display_hosts(self):
        log.info("=== Host Database ===")
        for mac, info in self.hosts.items():
            log.info("MAC: %s | IP: %s | Switch: %s | Port: %s", mac, info['ip'], info['dpid'], info['port'])

def launch():
    core.registerNew(HostDiscovery)
