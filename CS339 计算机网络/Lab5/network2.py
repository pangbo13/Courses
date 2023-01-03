#!/usr/bin/python3

"""
Simple example of setting network and CPU parameters  
"""

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSBridge
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import quietRun, dumpNodeConnections
from mininet.log import setLogLevel, info
from mininet.cli import CLI

from sys import argv
import time

# It would be nice if we didn't have to do this:
# pylint: disable=arguments-differ

class SingleSwitchTopo( Topo ):
    def build( self ):
        switch1 = self.addSwitch('s1')
        switch2 = self.addSwitch('s2')
        host1 = self.addHost('h1')
        host2 = self.addHost('h2')
        host3 = self.addHost('h3')
        host4 = self.addHost('h4')
        self.addLink(host1, switch1, bw=100, delay='5ms', loss=0, use_htb=True)
        self.addLink(host2, switch2, bw=100, delay='5ms', loss=0, use_htb=True)
        self.addLink(host3, switch1, bw=100, delay='5ms', loss=0, use_htb=True)
        self.addLink(host4, switch2, bw=100, delay='5ms', loss=0, use_htb=True)
        self.addLink(switch1, switch2, bw=100, delay='200ms', loss=0.1, use_htb=True)

def Test(tcp):
    "Create network and run simple performance test"
    topo = SingleSwitchTopo()
    net = Mininet( topo=topo,
                   host=CPULimitedHost, link=TCLink,
                   autoStaticArp=False )
    net.start()
    info( "Dumping host connections\n" )
    dumpNodeConnections(net.hosts)
    # set up tcp congestion control algorithm
    output = quietRun( 'sysctl -w net.ipv4.tcp_congestion_control=' + tcp )
    assert tcp in output
    info( "Testing bandwidth between h1 and h2 under TCP " + tcp + "\n" )
    h1, h2 = net.getNodeByName('h1', 'h2')
    # _serverbw, clientbw = net.iperf( [ h1, h2 ], seconds=10 )
    # info( clientbw, '\n' )
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    # pick a congestion control algorithm, for example, 'reno', 'cubic', 'bbr', 'vegas', 'hybla', etc.
    tcp = 'reno'
    Test(tcp)
