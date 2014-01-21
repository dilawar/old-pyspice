#!/usr/bin/env python

"""circuit.py: 

Last modified: Tue Jan 21, 2014  12:32AM

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2013, NCBS Bangalore"
__credits__          = ["NCBS Bangalore", "Bhalla Lab"]
__license__          = "GPL"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@iitb.ac.in"
__status__           = "Development"


import os 
import sys
import networkx as nx
from device import *
import logging
import matplotlib.pyplot as plt
from circuit import *
from debug import *

logging.basicConfig(level=logging.DEBUG)

class Node:
    """
    Class representing node.
    """
    def __init__(self):
        self.name = ""
        self.index = 0


class Circuit():
    '''
    Circtuit class.
    '''
    def __init__(self, name="circuit"):
        self.name = name
        self.nodeSet = set()
        self.deviceSet = set()
        self.devices = dict()

    def draw(self, fileName=None):
        nx.draw(network)
        if fileName: plt.savefig(fileName)
        else: plt.show()

    def toTikz(self):
        """This function writes the circuit into tikz description 
        TODO: We should export fabric of circuit to tikz. Before that it would
        not make much sense. 
        Fabric class is yet to be implemented. Currently we are only working
        with graph-based topology.

        """
        self.tikzDir = 'tikz'
        if not os.isdir(self.tikzDir):
            os.makedirs(self.tikzDir)
        
        doc = []
        doc.append("\documentclass[tikz]"+ "{standalone}")
        doc.append("\document{document}")
        doc.append("\begin{figure}")
        doc.append("\centering")
        doc.append("\begin{tikzpicture}")

    def getDevice(self, deviceName):
        '''Get the device when device name '''
        for es in network.edges():
            for e in network[es[0]][es[1]].values():
                if e['label'] == deviceName:
                    return e
        return None

    def addDevice(self, d, **kwargs):
        '''Add a device to network.
        '''
        if d.name not in self.deviceSet: 
            self.deviceSet.add(d.name)
        else:
            logging.warning("Device already added")
            return 

        if isinstance(d, Resistor):
            self.addLinearDevice(d)
        elif isinstance(d, Capacitor):
            self.addLinearDevice(d)
        else:
            raise UserWarning("This device %s is not supported" % d)

    def addDevices(self, devices):
        [self.addDevice(d) for d in devices]

    def addLinearDevice(self, d):
        ''' Add a linear device '''
        assert len(d.inputP) == 1, d.input
        assert len(d.outputP) == 1, d.output
        n1 = d.inputP[-1]
        n2 = d.outputP[-1]
        if n1 not in self.nodeSet:
            self.nodeSet.add(n1)
        if n2 not in self.nodeSet:
            self.nodeSet.add(n2)
        network.add_edge(n1, n2, label=d.name, device=d)
        assert len(network) == len(self.nodeSet)

    def toGraphviz(self):
        ''' Convert the graph to graphviz file.'''
        pass

    def inSeries(self, devices):
        '''
        Pop the first device from front. and recurse over the length of the
        devices. Till only one device is left.

        After pop, first device is copied into second device. Its input and
        output ports are rewritten. and both are connected in series.
        '''
        assert len(devices) > 1, "More than one device is needed for series"
        while(len(devices) > 1):
            firstD = devices.pop(0)
            if len(firstD.inputP) < 1 or len(firstD.outputP) < 1:
                printDebug("INFO"
                        , "First device must have both input and output port" + 
                        " well defined."
                        )
                sys.exit()
            self.addDevice(firstD)

            secondD = devices[0]
            if len(secondD.inputP) > 0 or len(secondD.outputP) > 0:
                printDebug("INFO"
                        , "Overwriting input and/or output ports {} -> {}".format(
                            secondD.inputP, secondD.outputP
                            )
                        )
            
            logging.info("Adding {} and {} in-series".format(firstD, secondD))
            
            secondD.setPort(None, None)
            secondD.inputP = firstD.outputP[:]
            self.addDevice(secondD)

    def inParallel(self, devices):
        '''Add devices in parallel.
        '''
        assert len(devices) > 1, "More than one device is needed for parallel"
        while(len(devices) > 1):
            firstD = devices.pop(0)
            if len(firstD.inputP) < 1 or len(firstD.outputP) < 1:
                raise UserWarning, "Missing value or parameter"
            if len(secondD.inputP) < 1 or len(secondD.outputP) < 1:
                raise UserWarning, "Missing value or parameter"
            self.addDevice(firstD)

            secondD = devices[0]

            logging.info("Adding {} and {} in-parallel".format(firstD, secondD))
            secondD.inputP = firstD.outputP[:]
            secondD.outputP = firstD.inputP[:]
            self.addDevice(secondD)

if __name__ == "__main__":
    print("Constucting a circuit")
    c = Circuit("compartment")
    r = Resistor('ra1', 1.0, 'pI1', 'pI2'
            , comment = "This resister do the coupling" )
    c.addDevice(r)
    r1 = Resistor('ra2', 1.0, 'pI2', 'pI3')
    c1 = Capacitor('ca1', 1e6)
    c.inSeries([r1, c1])
    c.draw('circuit.eps')

