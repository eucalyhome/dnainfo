#!/usr/bin/env python

import serial
import re
import sys
import time

#output : W F V A ohm VBAT measW Funit
class dnaconnect:
    dnadevicename = '/dev/ttyACM0'

    def readdata(self):
        (temp,dnab) = self._getdata("B=GET")
        if temp == "notfound":
            sys.exit()
        (dnawstring,dnaw) = self._getdata("P=GET")
        recheck = dnawstring.find("?")
        if recheck != -1:
            return ["wait","","","","",dnab,"",""]
        recheck = dnawstring.find("W")
        if recheck == -1:
            self.reconnectdna()
        dnatv = "F"
        (dnatstring,dnat) = self._getdata("T=GET")
        recheck = dnatstring.find("C")
        if recheck != -1:
            dnatv = "C"
        (temp,dnav) = self._getdata("V=GET RAW")
        (temp,dnai) = self._getdata("I=GET RAW")
        (temp,dnar) = self._getdata("R=GET LIVE")
        dnamw = float(dnav * dnai)
        if dnamw < 0:
            dnamw = 0
        return [dnaw,dnat,dnav,dnai,dnar,dnab,dnamw,dnatv]

    def initdna(self):
        try:
            self.serialhandle = serial.Serial(self.dnadevicename, 115200, timeout=0.03)
            return()
        except:
            sys.exit()

    def reconnectdna(self):
        try:
            self.serialhandle.close()
        except:
            pass
        sleep(0.05)
        self.initdna()

    def _getdata(self,querydata):
        while True:
            try:
                outputstring = querydata + "\n"
                self.serialhandle.flush()
                self.serialhandle.write(bytes(outputstring))
                serialline = self.serialhandle.readline()
                serialline = serialline.strip()
                seriallinedigit = self._getdigit(serialline)
                return (serialline,seriallinedigit)
            except IOError:
                self.serialhandle.close
                return("notfound","")

    def _getdigit(self,querydata):
        digit = re.search(r"[-\d\.]+", querydata)
        if digit is None:
            result = 0
        else:
            result =  float(digit.group())
        return (result)

