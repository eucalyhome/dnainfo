#!/usr/bin/env python

import os,time

def main():
    while True:
        if os.path.exists("/dev/ttyACM0"):
            try:
                time.sleep(0.05)
                os.system("/usr/bin/perl /data/dnainfo/rckick null")
                os.system("/usr/bin/python /data/dnainfo/dnainfomain.py")
            except:
                pass
        try:
            os.system("/usr/bin/python /data/dnainfo/dnainfotitle.py")
        except:
            os.exit()

if __name__ == '__main__':
    main()