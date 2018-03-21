#!/usr/bin/env python

import dnainfoledrender, dnainfoconnect, time, os

def viewswitch():
    rcfile = '/ramdisk/rcdata'
    global viewswitchflag
    global wattmeasflag
    global viewdata
    global targetslot
    rcdata = open(rcfile).read()
    rcflag = 0
    if rcdata == "rckey_volup":
        viewswitchflag = viewswitchflag + 1
        rcflag = 1
    elif rcdata == "rckey_voldown":
        viewswitchflag = viewswitchflag - 1
#        viewdata.ledimagesave()
        rcflag = 1
    if rcdata == "rckey_rr":
        targetslot = targetslot + 1
        if targetslot > 9:
            targetslot = 0
        if targetslot == 0:
            viewdata.setupinfo("CURRENT",0.5)
        else:
            viewtargetslot = targetslot
            viewdata.setupinfo("HIST " + (str(viewtargetslot)),0.5)
        rcflag = 1
    elif rcdata == "rckey_ff":
        targetslot = targetslot - 1
        if targetslot < 0:
            targetslot = 9
        if targetslot == 0:
            viewdata.setupinfo("CURRENT",0.5)
        else:
            viewtargetslot = targetslot
            viewdata.setupinfo("HIST " + (str(viewtargetslot)),0.5)
        rcflag = 1
    elif rcdata == "rckey_play":
        targetslot = 0
        viewdata.setupinfo("CURRENT",0.5)
        rcflag = 1
    elif rcdata == "rckey_menu":
        wattmeasflag = wattmeasflag + 1
        if wattmeasflag > 1:
            wattmeasflag = 0
            viewdata.setupinfo("DNA WATT",0.5)
        else:
            viewdata.setupinfo("MEAS WATT",0.5)
        rcflag = 1
    if rcflag == 1:
        rcdata = "."
        f = open(rcfile, 'w')
        f.write(rcdata)
        f.close()
        viewdata.ledclear()
    if viewswitchflag > 4:
        viewswitchflag = 0
    if viewswitchflag < 0:
        viewswitchflag = 4
    wattviewdata = 0
    if wattmeasflag == 1:
        wattviewdata = 6
    if viewswitchflag == 0:
        viewdata.writegraph([wattviewdata,1,4],targetslot)
    elif viewswitchflag == 1:
        viewdata.moduleview([2,3,4,wattviewdata],targetslot)
    elif viewswitchflag == 2:
        viewdata.stddivview(wattviewdata,targetslot)
    elif viewswitchflag == 3:
        viewdata.totalview(wattviewdata,targetslot)
    elif viewswitchflag == 4:
        viewdata.bathelthview(targetslot)
    viewdata.ledoutput()

def main():
    global viewswitchflag
    global wattmeasflag
    global viewdata
    global targetslot
    viewswitchflag = 0
    wattmeasflag = 0
    targetslot = 0

    dnaconnectdata = dnainfoconnect.dnaconnect()
    dnaconnectdata.initdna()
    viewdata = dnainfoledrender.ledrender()
    viewdata.loadfonts()
    viewdata.ledinit()
    viewdata.processinit(["W","F","V","A","o","V","W"])
    viewdata.datainit(["W","F","V","A","o","V","W"])
    viewinitflag = 0

    while True:
        dnaresult = dnaconnectdata.readdata()
        if dnaresult[0] != "wait":
            viewdata.datainit(["W","F","V","A","o","V","W"])
            targetslot = 0
            for seconddata in range(200):
                timestart = time.time()
                dnaresult = dnaconnectdata.readdata()
                if dnaresult[0] == "wait":
                    break
                viewdata.datarec(dnaresult)
                viewswitch()
                timeend = time.time()
                timesleep = timeend - timestart
                timesleep = 0.1 - timesleep
                if (timesleep < 0):
                    pass
                else:
                    time.sleep(timesleep)
        else:
            viewswitch()
            viewdata.setbatstaticvoltage(dnaresult[5])
            time.sleep(0.05)
            viewinitflag = 1

if __name__ == '__main__':
    main()
