#!/usr/bin/env python3

from sys import argv

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Host
from mininet.link import TCLink
from mininet.util import dumpNodeConnections,irange
from mininet.log import setLogLevel, info
from mininet.cli import CLI,quietRun

class TripleSwitchTopo(Topo):
    def build(self):
        switchs = dict([(f"s{switch_id}",self.addSwitch(f"s{switch_id}")) for switch_id in irange(1,3)])
        hosts = dict([(f"h{host_id}",self.addHost(f"h{host_id}")) for host_id in irange(1,3)])
        self.addLink("h1", "s1", use_htb=True)
        self.addLink("s1", "s2", bw=10, loss=5, use_htb=True)
        self.addLink("h2", "s2", use_htb=True)
        self.addLink("s1", "s3", bw=10, loss=5, use_htb=True)
        self.addLink("h3", "s3", use_htb=True)
        self.addLink("s2", "s3", use_htb=True)



def main():
    "Create network and run simple performance test"
    topo = TripleSwitchTopo()
    net = Mininet( topo=topo,
                   host=Host, link=TCLink,
                   autoStaticArp=True )
    net.start()
    info( "Dumping host connections\n" )
    dumpNodeConnections(net.hosts)
    info( "Dumping switch connections\n" )
    dumpNodeConnections(net.switches)

    quietRun("ovs-ofctl add-flow s1 in_port=s1-eth1,actions=output:all")
    quietRun("ovs-ofctl add-flow s2 in_port=s2-eth2,actions=output:all")
    quietRun("ovs-ofctl add-flow s3 in_port=s3-eth2,actions=output:all")
    quietRun("ovs-ofctl add-flow s1 in_port=s1-eth2,actions=output:s1-eth1")
    quietRun("ovs-ofctl add-flow s1 in_port=s1-eth3,actions=output:s1-eth1")
    quietRun("ovs-ofctl add-flow s2 in_port=s2-eth1,actions=output:s2-eth2")
    quietRun("ovs-ofctl add-flow s2 in_port=s2-eth3,actions=output:s2-eth2")
    quietRun("ovs-ofctl add-flow s3 in_port=s3-eth1,actions=output:s3-eth2")
    quietRun("ovs-ofctl add-flow s3 in_port=s3-eth3,actions=output:s3-eth2")

    net.pingAll()

    h1, h2, h3 = net.getNodeByName('h1', 'h2', 'h3')
    net.iperf(( h1, h2 ))
    net.iperf(( h1, h3 ))
    net.iperf(( h2, h3 ))

    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel( 'info' )
    main()
