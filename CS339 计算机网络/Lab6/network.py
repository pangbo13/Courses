#!/usr/bin/python3

"""
Sample Code
"""

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSBridge, OVSSwitch, OVSKernelSwitch
from mininet.node import CPULimitedHost
from mininet.node import RemoteController
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from sys import argv

# It would be nice if we didn't have to do this:
# pylint: disable=arguments-differ

def Test():
    "Create network and run simple performance test"
    net = Mininet( switch=OVSSwitch,
                   host=CPULimitedHost, link=TCLink,
                   autoStaticArp=False, controller=RemoteController)
    switch1 = net.addSwitch('s1')
    switch2 = net.addSwitch('s2')
    switch3 = net.addSwitch('s3')
    switch4 = net.addSwitch('s4')
    host1 = net.addHost('h1', cpu=.25, mac='00:00:00:00:00:01')
    host2 = net.addHost('h2', cpu=.25, mac='00:00:00:00:00:02')
    net.addLink(host1, switch1, bw=10, delay='5ms', loss=0, use_htb=True)
    net.addLink(host2, switch2, bw=10, delay='5ms', loss=0, use_htb=True)
    net.addLink(switch1, switch3, bw=10, delay='5ms', loss=0, use_htb=True)
    net.addLink(switch1, switch4, bw=10, delay='5ms', loss=0, use_htb=True)
    net.addLink(switch2, switch3, bw=10, delay='5ms', loss=0, use_htb=True)
    net.addLink(switch2, switch4, bw=10, delay='5ms', loss=0, use_htb=True)
    c1 = net.addController('c1', controller=RemoteController, ip="127.0.0.1", port=6653)
    net.build()
    c1.start()
    s1, s2, s3, s4 = net.getNodeByName('s1', 's2', 's3', 's4')
    s1.start([c1])
    s2.start([c1])
    s3.start([c1])
    s4.start([c1])
    net.start()
    info( "Dumping host connections\n" )
    dumpNodeConnections(net.hosts)
    dumpNodeConnections(net.switches)
    h1, h2 = net.getNodeByName('h1', 'h2')
    CLI(net)
    net.stop()

if __name__ == '__main__':
    # setLogLevel( 'debug' )
    setLogLevel('info')
    Test()
