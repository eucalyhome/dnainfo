#!/usr/bin/env python

from PIL import Image, ImageDraw, ImageOps
from rgbmatrix import RGBMatrix, RGBMatrixOptions
import numpy
import time

class ledrender:
    imagedir = '/data/dnainfo/image/'
    ledoptions_hardware_mapping = 'adafruit-hat-pwm'
    ledoptions_led_rgb_sequence = 'RBG'
    ledoptions_rows = 32
    ledoptions_chain_length = 4
    ledoptions_parallel = 1
    ledoptions_pwm_bits = 11
    ledoptions_brightness = 50
    ledoptions_pwm_lsb_nanoseconds = 130

    largechars = []
    largeindex = []
    midiumchars = []
    midiumchars = []
    midiumindex = []
    smallchars = []
    smallindex = []
    smallcharscolor = [[]]
    targetarray = [[[]]]
    targetname = [[]]
    targetmax = [[]]
    targetarraylength = []

    def loadfonts(self):
        self.largeindex = ["0","1","2","3","4","5","6","7","8","9","W","V","A","-","o","."," "]
        imagedata = Image.open(self.imagedir + 'largefont.bmp', 'r')
        for i in range(16):
            startx =  ( i * 16 ) % 128
            starty = (int( i / 8 )) * 32
            self.largechars.append(imagedata.crop((startx, starty, startx+16, starty+32)))
        self.largechars.append(Image.new('RGB', (16, 32), (0, 0, 0)))

        self.midiumindex = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P",
                            "Q","R","S","T","U","V","W","X","Y","Z","o","z","z","z","z","z",
                            "0","1","2","3","4","5","6","7","8","9","-","*",">",".","m","z"," "]
        imagedata = Image.open(self.imagedir + '/midiumfont.bmp', 'r')
        for i in range(48):
            startx =  ( i * 8 ) % 128
            starty = (int( i / 16 )) * 16
            self.midiumchars.append(imagedata.crop((startx, starty, startx+8, starty+16)))
        self.midiumchars.append(Image.new('RGB', (8, 16), (0, 0, 0)))

        self.smallindex = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P",
                           "Q","R","S","T","U","V","W","X","Y","Z","o","z","z","z","z","z",
                           "0","1","2","3","4","5","6","7","8","9","-","*",">",".","z","z"," "]
        imagedata = Image.open(self.imagedir + 'smallfont.png', 'r')
        for i in range(48):
            startx =  ( i * 6 ) % 96
            starty = (int( i / 16 )) * 8
            self.smallchars.append(imagedata.crop((startx, starty, startx+6, starty+8)))
        self.smallchars.append(Image.new('RGB', (6, 8), (0, 0, 0)))

        self.smallcharscolor = [[0 for i in range(49)] for j in range(4)]
        for colorpalette in range(4):
            imagedata = Image.open(self.imagedir + 'smallfont.png', 'r')
            if colorpalette == 0:
                blackcolor = (192,192,0)
                whitecolor = (0,0,0)
            elif colorpalette == 1:
                blackcolor = (0,192,192)
                whitecolor = (0,0,0)
            elif colorpalette == 2:
                blackcolor = (192,0,192)
                whitecolor = (0,0,0)
            else:
                blackcolor = (0,0,0)
                whitecolor = (192,192,192)
            imagedatacolor = ImageOps.colorize((
                            ImageOps.grayscale(imagedata)),
                            black=blackcolor,
                            white=whitecolor)
            for i in range(48):
                startx =  ( i * 6 ) % 96
                starty = (int( i / 16 )) * 8
                self.smallcharscolor[colorpalette][i] = imagedatacolor.crop((startx, starty, startx+6, starty+8))
            self.smallcharscolor[colorpalette][48] = Image.new('RGB', (6, 8), blackcolor)


    def renderlargefont(self,col,name):
        col = col * 8
        self.ledcanvas.paste(self.largechars[(self.largeindex.index(name))],(col,0))

    def rendermidiumfont(self,col,row,name):
        col = col * 8
        row = row * 16
        self.ledcanvas.paste(self.midiumchars[(self.midiumindex.index(name))],(col,row))

    def rendersmallfont(self,col,row,name):
        col = col * 6
        row = row * 8
        self.ledcanvas.paste(self.smallchars[(self.smallindex.index(name))],(col,row))

    def rendersmallfontcolor(self,col,row,palettedata,name):
        col = col * 6
        row = row * 8
        self.ledcanvas.paste(self.smallcharscolor[palettedata][(self.smallindex.index(name))],(col,row))

    def datarec(self,dnaresult):
        for targetdata in range(7):
            self.targetarray[0][targetdata][self.targetarraylength[0]] = dnaresult[targetdata]
            if self.targetmax[0][targetdata] < dnaresult[targetdata]:
                self.targetmax[0][targetdata] = dnaresult[targetdata]
        self.targetarraylength[0] = self.targetarraylength[0] + 1
        self.targetname[0][1] = dnaresult[7]

    def processinit(self,targetnameentry):
        self.targetarray = [[[0 for i in range(200)] for j in range(7)]for k in range(10)]
        self.targetmax = [[0 for i in range(7)] for j in range(10)]
        self.targetname = [[0 for i in range(7)] for j in range(10)]
        for targetslot in range(10):
            for targetdata in range(7):
                self.targetname[targetslot][targetdata] = targetnameentry [targetdata]
        self.targetarraylength = [0 for i in range(10)]
        self.batstaticvoltage = 4.2
        self.infostring = ""

    def datainit(self,targetnameentry):
        for i in range(9):
            k = 8 - i
            j = k + 1
            self.targetarray[j][:] = self.targetarray[k][:]
            self.targetmax[j][:] = self.targetmax[k][:]
            self.targetname[j][:] = self.targetname[k][:]
            self.targetarraylength[j] = self.targetarraylength[k]
        self.targetarray[0] = [[0 for i in range(200)] for j in range(7)]
        self.targetmax[0] = [0 for i in range(7)]
        self.targetname[0] = [0 for i in range(7)]
        for targetdata in range(7):
            self.targetname[0][targetdata] = targetnameentry [targetdata]
        self.targetarraylength[0] = 0

    def setbatstaticvoltage(self,batvoltage):
        self.batstaticvoltage = batvoltage

    def writegraph(self,graphtargetdata,targetslot):
        drawcanvas = ImageDraw.Draw(self.ledcanvas)
        drawcanvas.rectangle((30, 0, 127, 31), fill=(0, 0, 0), outline=(80, 80, 80))

        if self.targetarraylength[targetslot] > 0:
            targetlength = self.targetarraylength[targetslot] - 1
        else:
            targetlength = 0
        for targetdata in range(3):
            outputstr = self.targetarray[targetslot][graphtargetdata[targetdata]][targetlength]
            if outputstr > 10000:
                outputstr = "9999"
            elif outputstr > 100:
                outputstr = "{0:4.0f}".format(outputstr)
            elif outputstr > 10:
                outputstr ="{0:4.01f}".format(outputstr)
            else:
                outputstr = "{0:4.02f}".format(outputstr)
            for i in range(4):
                self.rendersmallfontcolor(i,targetdata,targetdata,outputstr[i])
            self.rendersmallfontcolor(4,targetdata,targetdata,self.targetname[targetslot][graphtargetdata[targetdata]])
        outputstr = "{0:4.1f}".format(float(self.targetarraylength[targetslot]) / 10)
        for i in range(4):
            self.rendersmallfontcolor(i,3,3,outputstr[i])
        self.rendersmallfontcolor(4,3,3,"S")

        if self.targetarraylength[targetslot] < 12:
            graphmultiply = 8
        elif self.targetarraylength[targetslot] < 24:
            graphmultiply = 4
        elif self.targetarraylength[targetslot] < 48:
            graphmultiply = 2
        elif self.targetarraylength[targetslot] < 96:
            graphmultiply = 1
        else:
            graphmultiply = 0

        for targetdata in range(3):
            if targetdata == 0:
                targetcolor = (255,255,0)
            elif targetdata == 1:
                targetcolor = (0,255,255)
            else:
                targetcolor = (255,0,255)

            graphmaxdiv = self.targetmax[targetslot][graphtargetdata[targetdata]] / 30
            for i in range(96):
                if graphmultiply == 0:
                    graphpointcount = i * 2
                else:
                    graphpointcount = int (i / graphmultiply)
                if self.targetarray[targetslot][graphtargetdata[targetdata]][graphpointcount] > 0:
                    graphdata = self.targetarray[targetslot][graphtargetdata[targetdata]][graphpointcount]
                    graphy = 30 - int (graphdata / graphmaxdiv)
                    graphx = i + 31
                    drawcanvas.point((graphx,graphy), fill=targetcolor)

    def moduleview(self,graphtargetdata,targetslot):
        drawcanvas = ImageDraw.Draw(self.ledcanvas)

        targetlength = self.targetarraylength[targetslot] - 1
        for targetdata in range(3):
            outputstr = self._formatstrfour(self.targetarray[targetslot][graphtargetdata[targetdata]][targetlength])
            for i in range(4):
                self.rendersmallfont(i,targetdata,outputstr[i])
            self.rendersmallfont(4,targetdata,self.targetname[targetslot][graphtargetdata[targetdata]])
        outputstr = "{0:4.1f}".format(float(self.targetarraylength[targetslot]) / 10)
        for i in range(4):
            self.rendersmallfont(i,3,outputstr[i])
        self.rendersmallfont(4,3,"S")

        outputstr = self.targetarray[targetslot][graphtargetdata[3]][targetlength]
        if outputstr > 10000:
            outputstr = "99999"
        elif outputstr > 1000:
            outputstr = "{0:5.0f}".format(outputstr)
            outputdot = 0
        elif outputstr > 100:
            outputstr = "{0:5.01f}".format(outputstr)
            outputdot = 4
        elif outputstr > 10:
            outputstr ="{0:5.02f}".format(outputstr)
            outputdot = 3
        else:
            outputstr = "{0:5.03f}".format(outputstr)
            outputdot = 2
        if outputdot == 0:
            fontcolpoint = 2
        else:
            fontcolpoint = 3
        for i in range(5):
            if i == outputdot and i != 0:
                fontcolpoint = fontcolpoint + 1
            else:
                fontcolpoint = fontcolpoint + 2
            self.renderlargefont(fontcolpoint,outputstr[i])
        self.renderlargefont(14,self.targetname[targetslot][graphtargetdata[3]])

    def stddivview(self,targetdata,targetslot):
        self._rawdataview(targetdata,targetslot)
        if self.targetarraylength[targetslot] > 0:
            targetlength = self.targetarraylength[targetslot] - 1
        else:
            targetlength = 0
        stddata = []
        for i in range(targetlength):
            stddata.append(self.targetarray[targetslot][targetdata][i])
        if targetlength > 2:
            outputstr = numpy.std(stddata)
        else:
            outputstr = 0
        outputstr = self._formatstrfive(outputstr)
        outputstr = "  STD-DIV> " + outputstr
        for i in range(16):
            self.rendermidiumfont(i,1,outputstr[i])

    def totalview(self,targetdata,targetslot):
        self._rawdataview(targetdata,targetslot)
        if self.targetarraylength[targetslot] > 0:
            targetlength = self.targetarraylength[targetslot] - 1
        else:
            targetlength = 0
        totaldata = 0
        for i in range(targetlength):
            totaldata = totaldata + self.targetarray[targetslot][targetdata][i]
        if targetlength > 2:
            outputstr = totaldata * 100 / 3600
        else:
            outputstr = 0
        outputstr = self._formatstrfive(outputstr)
        outputstr = " TOTAL> " + outputstr + "m" + self.targetname[targetslot][targetdata] + "H"
        for i in range(16):
            self.rendermidiumfont(i,1,outputstr[i])

    def bathelthview(self,targetslot):
        staticvoltage = float(self.batstaticvoltage)

        if self.targetarraylength[targetslot] > 0:
            targetlength = self.targetarraylength[targetslot] - 1
        else:
            targetlength = 0
        realvoltage = self.targetarray[targetslot][5][targetlength]
        if (realvoltage < 1) or (targetlength == 0) or (self.targetarray[targetslot][2][targetlength] < 0) or (self.targetarray[targetslot][3][targetlength] < 0):
            realvoltage = 1
            outputstr = "  NOT CALC BAT HEALTH"
            for i in range(len(outputstr)):
                self.rendersmallfont(i,2,outputstr[i])
            return()
        deltavoltage = staticvoltage - realvoltage
        if deltavoltage < 0.01:
            deltavoltage = 0.01
        realwatt = self.targetarray[targetslot][2][targetlength] * self.targetarray[targetslot][3][targetlength]
        loadwatt = realwatt / 8
        loadwatt = loadwatt * 10
        inneramp = loadwatt / realvoltage
        if inneramp < 0.1:
            inneramp = 0.1
        innerohm = deltavoltage / inneramp
        innerohm = innerohm * 1000
        outputstaticvoltage = self._formatstrfour(staticvoltage)
        outputrealvoltage = self._formatstrfour(realvoltage)
        outputdeltavoltage = self._formatstrfour(deltavoltage)
        outputrealwatt = self._formatstrfour(realwatt)
        outputdnavoltage = self._formatstrfour(self.targetarray[targetslot][2][targetlength])
        outputdnaamp = self._formatstrfour(self.targetarray[targetslot][3][targetlength])
        outputinnerohm = self._formatstrfive(innerohm)

        outputstr = "OFF " + outputstaticvoltage + "V"
        for i in range(len(outputstr)):
            self.rendersmallfont(i,0,outputstr[i])
        outputstr = " ON " + outputrealvoltage + "V"
        for i in range(len(outputstr)):
            self.rendersmallfont(i,1,outputstr[i])
        outputstr = "DLT " + outputdeltavoltage + "V  BAT HEALTH"
        for i in range(len(outputstr)):
           self.rendersmallfont(i,2,outputstr[i])
        outputstr = "OUT " + outputdnavoltage + "V " + outputdnaamp + "A " + outputrealwatt + "W"
        for i in range(len(outputstr)):
            self.rendersmallfont(i,3,outputstr[i])

        fontcolpoint = 7
        outputstr = outputinnerohm + "mo"
        for i in range(7):
            fontcolpoint = fontcolpoint + 1
            self.rendermidiumfont(fontcolpoint,0,outputstr[i])

    def _rawdataview(self,targetdata,targetslot):
        drawcanvas = ImageDraw.Draw(self.ledcanvas)
        if self.targetarraylength[targetslot] > 0:
            targetlength = self.targetarraylength[targetslot] - 1
        else:
            targetlength = 0
        outputstr = self.targetarray[targetslot][targetdata][targetlength]
        outputstr = self._formatstrfive(outputstr)
        for i in range(5):
            self.rendermidiumfont(i,0,outputstr[i])
        self.rendermidiumfont(5,0,self.targetname[targetslot][targetdata])
        outputstr = "{0:4.1f}".format(float(self.targetarraylength[targetslot]) / 10)
        fontcolpoint = 6
        for i in range(4):
            fontcolpoint = fontcolpoint + 1
            self.rendermidiumfont(fontcolpoint,0,outputstr[i])
        self.rendermidiumfont(11,0,"S")

    def _formatstrfive(self,outputstr):
        if outputstr > 10000:
            outputstr = "99999"
        elif outputstr > 1000:
            outputstr = "{0:5.0f}".format(outputstr)
        elif outputstr > 100:
            outputstr = "{0:5.01f}".format(outputstr)
        elif outputstr > 10:
            outputstr ="{0:5.02f}".format(outputstr)
        else:
            outputstr = "{0:5.03f}".format(outputstr)
        return (outputstr)

    def _formatstrfour(self,outputstr):
        if outputstr > 10000:
            outputstr = "9999"
        elif outputstr > 100:
            outputstr = "{0:4.0f}".format(outputstr)
        elif outputstr > 10:
            outputstr ="{0:4.01f}".format(outputstr)
        else:
            outputstr = "{0:4.02f}".format(outputstr)
        return (outputstr)

    def setupinfo(self,targetstring,targettime):
        if targetstring == "":
            self.infostring = ""
            return()
        self.infostartpoint = 20 - (len(targetstring))
        self.infostring = targetstring
        timenow = time.time()
        self.infotime = timenow + targettime

    def _outputinfo(self):
        if self.infostring == "":
            return()
        timenow = time.time()
        if self.infotime < timenow:
           self.infostring = ""
           return()
        for i in range(len(self.infostring)):
            fontcol = i + self.infostartpoint
            self.rendersmallfontcolor(fontcol,3,3,self.infostring[i])

    def ledinit(self):
        self.options = RGBMatrixOptions()
        self.options.hardware_mapping = self.ledoptions_hardware_mapping
        self.options.led_rgb_sequence = self.ledoptions_led_rgb_sequence
        self.options.rows = self.ledoptions_rows
        self.options.chain_length = self.ledoptions_chain_length
        self.options.parallel = self.ledoptions_parallel
        self.options.pwm_bits = self.ledoptions_pwm_bits
        self.options.brightness = self.ledoptions_brightness
        self.options.pwm_lsb_nanoseconds = self.ledoptions_pwm_lsb_nanoseconds
        self.matrix = RGBMatrix(options = self.options)
        self.ledcanvas = Image.new('RGB', (128, 32), (0, 0, 0))

    def ledclear(self):
        self.ledcanvas = Image.new('RGB', (128, 32), (0, 0, 0))

    def ledtitle(self):
        self.ledcanvas = Image.open(self.imagedir + 'title.png', 'r').convert('RGB')
        self.matrix.SetImage(self.ledcanvas)

    def ledoutput(self):
        self._outputinfo()
        self.matrix.SetImage(self.ledcanvas)

    def ledimagesave(self):
        self._outputinfo()
        timenowsaveimage = str(time.time())
        self.ledcanvas.save(self.imagedir + 'ledimagedata' + timenowsaveimage + ".png")