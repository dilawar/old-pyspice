#!/usr/bin/env python3
import circuit.circuit as cir

if __name__ == "__main__" :
    print("Constucting a circuit")
    c = cir.Circuit("compartment")
    r = cir.Resistor('ra1', 1.0
            , comment = "This resister do the coupling" )
    r1 = cir.Resistor('ra1', 1.0)
    r2 = cir.Resistor('ra2', 1.0)
    c.inSeries([r1, r2])
    cm = cir.Capacitor('cm', 1e-9)

    c.draw('circuit.eps')

