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

logging.basicConfig(level=logging.DEBUG)

class Node:
    """
    Class representing node.
    """
    def __init__(self):
        self.name = ""
        self.index = 0


class Circuit:
    '''
    Circtuit class.
    '''
    def __init__(self, name="circuit"):
        self.name = name
        self.graph = nx.MultiDiGraph(name=self.name)
        self.nodeSet = set()
        self.deviceSet = set()
        self.devices = dict()

    def draw(self, fileName=None):
        nx.draw(self.graph)
        if fileName:
            plt.savefig(fileName)
        else:
            plt.show()

    def getDevice(self, deviceName):
        '''Get the device when device name '''
        for es in self.graph.edges():
            for e in self.graph[es[0]][es[1]].values():
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
        assert len(d.input) == 1, d.input
        assert len(d.output) == 1, d.output
        n1 = d.input[-1]
        n2 = d.output[-1]
        if n1 not in self.nodeSet:
            self.nodeSet.add(n1)
        if n2 not in self.nodeSet:
            self.nodeSet.add(n2)
        self.graph.add_edge(n1, n2, label=d.name, device=d)
        assert len(self.graph) == len(self.nodeSet)

    def toGraphviz(self):
        ''' Convert the graph to graphviz file.'''
        pass

    def inSeries(self, devices):
        assert len(devices) > 1, "More than one device is needed for series"
        while(len(devices) > 1):
            firstD = devices.pop(0)
            if len(firstD.input) < 1 or len(firstD.output) < 1:
                logging.error("Missing input and output port of base device")
                raise UserWarning, "Missing value or parameter"
            self.addDevice(firstD)

            secondD = devices[0]
            if len(secondD.input) > 0 or len(secondD.output) > 0:
                print("Overwriting input and/or output ports")
            
            logging.info("Adding {} and {} in-series".format(firstD, secondD))
            secondD.input = firstD.output[:]
            secondD.output = [secondD.name+'_out']
            self.addDevice(secondD)

    def inParallel(self, devices):
        '''Add devices in parallel.
        '''
        assert len(devices) > 1, "More than one device is needed for parallel"
        while(len(devices) > 1):
            firstD = devices.pop(0)
            if len(firstD.input) < 1 or len(firstD.output) < 1:
                raise UserWarning, "Missing value or parameter"
            if len(secondD.input) < 1 or len(secondD.output) < 1:
                raise UserWarning, "Missing value or parameter"
            self.addDevice(firstD)

            secondD = devices[0]

            logging.info("Adding {} and {} in-parallel".format(firstD, secondD))
            secondD.input = firstD.output[:]
            secondD.output = firstD.input[:]
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

