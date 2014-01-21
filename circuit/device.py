#!/usr/bin/env python

"""devices.py: This file contain classes of basic ngspice devices.

Last modified: Tue Jan 21, 2014  12:19AM

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2013, NCBS Bangalore"
__credits__          = ["NCBS Bangalore", "Bhalla Lab"]
__license__          = "GPL"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@iitb.ac.in"
__status__           = "Development"

import logging
import networkx as nx
from network import *

class Device(object):
    """
    Base class for all devices.
    """
    def __init__(self, paramDict):
        self.name = None
        self.spiceLine = None
        self.portNos = 2
        self.graphLine = None
        self.value = None
        self.inputP = []
        self.outputP = []
        self.current = 0.0
        self.voltage = 0.0
        self.params = paramDict

    def computeV(self, current):
        return current

    def computeI(self, voltage):
        return voltage 

    def setPort(self, inPort, outPort, append=False):
        '''Set the port of device 
        
        '''
        if not inPort:
            inPort = "ni_{}".format(len(network))
        if append: self.inputP.append(inPort)
        else: self.inputP = [inPort]

        if not outPort:
            outPort = "no_{}".format(len(network))
        if append: self.outputP.append(outPort)
        else: self.outputP = [ outPort ]

    def setParams(self, name, inPort, outPort):
        ''' Set parameters '''
        assert name, "Empty name"
        self.name = name
        self.setPort(inPort, outPort)

class Resistor(Device):
    """
    Implement register
    """

    def __init__(self, name, value=1.0, inT=None, outT=None, **kwargs):
        super(Resistor, self).__init__(kwargs)
        if not name:
            raise NameError("Missing name of device")
        if value == 0.0:
            raise ValueError("Zero or negative value of R: %s" % value)
        else:
            self.value = value
        self.setParams(name, inT, outT)

class Capacitor(Device):
    def __init__(self, name=None, value=0e-10, inT='', outT='', **kwargs):
        super(Capacitor, self).__init__(kwargs)
        self.name = name
        self.value = value 
        self.setParams(name, inT, outT)

class VoltageSource(Device):

    def __init__(self, name, value=1.0, inT='', outT='', **kwargs):
        super(VoltageSource, self).__init__(kwargs)
        self.value = value
        self.setParams(name, inT, outT)

