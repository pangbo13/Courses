#!/usr/bin/env python3

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Host
from mininet.link import TCLink
from mininet.util import dumpNodeConnections,irange
from mininet.log import setLogLevel, info

class TripleSwitchTopo( Topo ):

    def build(self):
        switchs = dict([(f"s{switch_id}",self.addSwitch(f"s{switch_id}")) for switch_id in irange(1,3)])
        hosts = dict([(f"h{host_id}",self.addHost(f"h{host_id}")) for host_id in irange(1,3)])

        self.addLink("s1", "s2", bw=10, loss=5, use_htb=True)
        self.addLink("s1", "s3", bw=10, loss=5, use_htb=True)
        self.addLink("h1", "s1", use_htb=True)
        self.addLink("h2", "s2", use_htb=True)
        self.addLink("h3", "s3", use_htb=True)

def main( lossy=True ):
    "Create network and run simple performance test"
    topo = TripleSwitchTopo()
    net = Mininet( topo=topo,
                   host=Host, link=TCLink,
                   autoStaticArp=True )
    net.start()
    info( "Dumping host connections\n" )
    dumpNodeConnections(net.hosts)
    
    net.pingAll()
    h1, h2, h3 = net.getNodeByName('h1', 'h2', 'h3')
    net.iperf(( h1, h2 ))
    net.iperf(( h1, h3 ))
    net.iperf(( h2, h3 ))

    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    main()
