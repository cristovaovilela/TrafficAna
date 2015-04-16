#!/usr/bin/python

import sys
import os.path
import urllib2
import numpy
import re
import datetime
from array import array
from subprocess import call

from ROOT import TFile, TTree, gROOT, TCanvas, TH2D, gStyle, TDatime

def drawShortestTimeInTraffic( ttreeName , drawOptions = "") :
    inFile = TFile(ttreeName+'.root')
    inTree = inFile.Get(ttreeName)
    
    histo = TH2D(ttreeName+'_hist', ttreeName, 144, 0, 24*60*60, 190, 0, 190)
    
    nEntries = inTree.GetEntries()
    
    year = numpy.zeros(1, dtype=int)
    month = numpy.zeros(1, dtype=int)
    day = numpy.zeros(1, dtype=int)
    hour = numpy.zeros(1, dtype=int)
    minute = numpy.zeros(1, dtype=int)
    weekday = numpy.zeros(1, dtype=int)

    distance = numpy.zeros(1, dtype=float)
    timeNoTraffic = numpy.zeros(1, dtype=int)
    timeInTraffic = numpy.zeros(1, dtype=int)
    
    inTree.SetBranchAddress('year', year)
    inTree.SetBranchAddress('month', month)
    inTree.SetBranchAddress('day', day)
    inTree.SetBranchAddress('hour', hour)
    inTree.SetBranchAddress('minute', minute)

    inTree.SetBranchAddress('timeInTraffic', timeInTraffic)

    # Get first entry
    inTree.GetEntry(0)
    oldDate = datetime.datetime(year[0], month[0], day[0], hour[0], minute[0], 0)
    minTrafficTime = timeInTraffic[0]

    for entry in range(0, nEntries) :
        inTree.GetEntry(entry)
        
        currentDate = datetime.datetime(year[0], month[0], day[0], hour[0], minute[0], 0)
        
        if (currentDate - oldDate).total_seconds() < (5*60) :
            print 'Comp times ', timeInTraffic[0], minTrafficTime
            if timeInTraffic[0] < minTrafficTime :
                minTrafficTime  = timeInTraffic[0]
                if entry == (nEntries -1) :
                    histo.Fill((oldDate.hour*60+oldDate.minute)*60, minTrafficTime)
        else :
            histo.Fill((oldDate.hour*60+oldDate.minute)*60, minTrafficTime)
            minTrafficTime = timeInTraffic[0]
            
        oldDate = currentDate

    histo.GetXaxis().SetTimeDisplay(1);
    histo.GetXaxis().SetTimeFormat("%H:%M");
        
    histo.Draw("COLZ")
    can.SaveAs("testPlot.pdf")

def main ():
    
    da = TDatime(2015,04,16,6,00,00);
    gStyle.SetTimeOffset(da.Convert());

    global can

    can = TCanvas()
    drawShortestTimeInTraffic(ttreeName='SBUToForestHills')
    




if __name__ == '__main__' :
    main()
