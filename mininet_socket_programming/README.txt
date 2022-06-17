Elliott Jensen
egjensen@ucsc.edu
egjensen

egjensen-lab3.pdf:
contains the solutions to and analysis to the lab problems

egjensen-lab3_controller.py
Contains the controller for the topography of the mininet network. It uses Open Flow.
Implements 3 rules: ICMP packets are allowed between subnet 1 and 3, TCP packeets are
allowed between subnets 1 and 2, and all other packets are dropped.

egjensen-lab3_topo.py
Contains the topography for mininet. Includes 5 hosts, 3 subnets and 3 switches