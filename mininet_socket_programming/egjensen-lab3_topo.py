#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import RemoteController

class final_topo(Topo):
  def build(self):

    h1 = self.addHost('h1',mac='00:00:00:00:00:01',ip='10.0.1.1/24', defaultRoute="h1-eth0")
    h2 = self.addHost('h2',mac='00:00:00:00:00:02',ip='10.0.1.2/24', defaultRoute="h2-eth0")
    h3 = self.addHost('h3',mac='00:00:00:00:00:03',ip='10.0.2.1/24', defaultRoute="h3-eth0")
    h4 = self.addHost('h4',mac='00:00:00:00:00:04',ip='10.0.2.2/24', defaultRoute="h4-eth0")
    h5 = self.addHost('h5',mac='00:00:00:00:00:05',ip='10.0.3.1/24', defaultRoute="h5-eth0")


    s1 = self.addSwitch('s1')
    s2 = self.addSwitch('s2')
    s3 = self.addSwitch('s3')

    self.addLink('s1', 's2', port1=1, port2=2)
    self.addLink('s2', 's3', port1=1, port2=2)
    self.addLink('s3', 's1', port1=1, port2=2)

    self.addLink('s1', 'h1', port1=3, port2=0)
    self.addLink('s1', 'h2', port1=4, port2=0)

    self.addLink('s2', 'h3', port1=3, port2=0)
    self.addLink('s2', 'h4', port1=4, port2=0)

    self.addLink('s3', 'h5', port1=3, port2=0)



def configure():
  topo = final_topo()
  net = Mininet(topo=topo, controller=RemoteController)
  net.start()
  # use static ARP
  net.staticArp() 
  CLI(net)
  
  net.stop()


if __name__ == '__main__':
  configure()
