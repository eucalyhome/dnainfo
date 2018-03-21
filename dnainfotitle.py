#!/usr/bin/env python

import dnainfoledrender,os,time

def main():
    dnadevicename = '/dev/ttyACM0'

    viewdata = dnainfoledrender.ledrender()
    viewdata.ledinit()
    viewdata.ledtitle()
    while True:
        if os.path.exists(dnadevicename):
            os.exit()
        time.sleep(2)


if __name__ == '__main__':
    main()