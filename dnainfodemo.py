#!/usr/bin/env python

import dnainfoconnect, os, time

def main():
    dnaconnectdata = dnainfoconnect.dnaconnect()
    dnaconnectdata.initdna()

    while True:
        dnaresult = dnaconnectdata.readdata()
        if dnaresult[0] != "wait":
            print str(dnaresult[0]) + "W ",
            print str(dnaresult[1]) + dnaresult[7] + " ",
            print str(dnaresult[2]) + "V ",
            print str(dnaresult[3]) + "A ",
            print str(dnaresult[4]) + "ohm ",
            print "BAT:",
            print str(dnaresult[5]) + "V ",
            print "MEAS WATT:",
            print str(dnaresult[6]) + "W"

if __name__ == '__main__':
    main()
