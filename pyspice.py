#!/usr/bin/env python3
import circuit.circuit as cir

if __name__ == "__main__" :
    print("Constucting a circuit")
    c = cir.Circuit("compartment")
    r = cir.Resistor('ra1', 1.0
            , comment = "This resister do the coupling" )
    r1 = cir.Resistor('ra2', 1.0)
    c1 = cir.Capacitor('ca1', 1e6)
    c.inSeries([r1, c1, r])
    c.draw('circuit.eps')

