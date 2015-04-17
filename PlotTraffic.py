#!/usr/bin/python

import sys
import os.path
import urllib2
import numpy
import re
import datetime
from array import array
from subprocess import call
from RouteList import *

from ROOT import TFile, TTree, gROOT, TCanvas, TH2D, gStyle, TDatime, TH1D, TProfile, TLegend, TLine, TArrow, TPad

def drawShortestTimeInTraffic( routeList , direction , fileName) :
    
    can = TCanvas("c"+direction, "c"+direction, 2000,1500)
    upperPad = TPad("upperPad", "upperPad", 0., 0.33, 1., 1.)
    upperPad.Draw()
    upperPad.SetGridy()
    lowerPad = TPad("lowerPad", "lowerPad", 0., 0., 1., 0.33)
    lowerPad.Draw()
    lowerPad.SetGridy()

    upperPad.cd()
    
    leg = TLegend(0.15, 0.76,0.85, 0.88)
    leg.SetNColumns(4)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)

    isFirst = True

    for route in routeList :

        if direction != route[4] :
            continue

        ttreeName = route[0]

        inFile = TFile(ttreeName+'.root')
        inTree = inFile.Get(ttreeName)
    
#        histo = TH2D(ttreeName+'_hist', ttreeName, 144, 0, 24*60*60, 190, 0, 190)
#        histo = TH2D(ttreeName+'_hist', ttreeName, 72, 0, 24*60*60, 190, 0, 190)
        histo          = TH2D(ttreeName+'_hist', ttreeName, 36, 0, 24*60*60, 190, 0, 190)
        histoNoTraffic = TH2D(ttreeName+'_histNoTraffic', ttreeName, 36, 0, 24*60*60, 190, 0, 190)
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
        inTree.SetBranchAddress('timeNoTraffic', timeNoTraffic)

        # Get first entry
        inTree.GetEntry(0)
        oldDate = datetime.datetime(year[0], month[0], day[0], hour[0], minute[0], 0)
        minTrafficTime = timeInTraffic[0]
        minNoTrafficTime = timeNoTraffic[0]

        for entry in range(0, nEntries) :
            inTree.GetEntry(entry)
        
            currentDate = datetime.datetime(year[0], month[0], day[0], hour[0], minute[0], 0)
        
            if (currentDate - oldDate).total_seconds() < (5*60) :
                if timeInTraffic[0] < minTrafficTime :
                    minTrafficTime  = timeInTraffic[0]
                    minNoTrafficTime = timeNoTraffic[0]
                    if entry == (nEntries -1) :
                        histo.Fill((oldDate.hour*60+oldDate.minute)*60, minTrafficTime)
                        histoNoTraffic.Fill((oldDate.hour*60+oldDate.minute)*60, minNoTrafficTime)
            else :
                histo.Fill((oldDate.hour*60+oldDate.minute)*60, minTrafficTime)
                histoNoTraffic.Fill((oldDate.hour*60+oldDate.minute)*60, minNoTrafficTime)
                minTrafficTime = timeInTraffic[0]
                minNoTrafficTime = timeNoTraffic[0]
                
            oldDate = currentDate

        
        histprof = TProfile(histo.ProfileX())
    
        histprof.SetLineColor(route[3])
        histprof.SetMarkerSize(0)
        
        if isFirst :
            isFirst=False
            histprof.GetXaxis().SetTimeDisplay(1);
            histprof.GetXaxis().SetTimeFormat("%H:%M");        
            histprof.SetMinimum(45.)
            histprof.SetMaximum(160.)
            histprof.SetTitle("Commute "+route[4]+";Time of departure;Duration in Traffic [minutes]")
            leg.AddEntry(histprof.DrawCopy("E1X0"), route[0], "l")
            print 'Drawing first', ttreeName
        else :
            print 'Drawing SAME', ttreeName
            leg.AddEntry(histprof.DrawCopy("SAMEE1X0"), route[0], "l")
        histprof.DrawCopy("SAMEHISTL][")
        
#        histprofNoTraffic = histoNoTraffic.ProfileX()
#        histprofNoTraffic.Add(histprof, -1)
#        histprofNoTraffic.SetMinimum(0.)
#        histprofNoTraffic.SetMaximum(60.)
#        histprofNoTraffic.GetYaxis().SetTitle("#Deltat (Traffic - NoTraffic) [minutes]")

#    lowerPad.cd()
#        if isFirst :
#            isFirst = False
#            histprofNoTraffic.DrawCopy("HIST")
#        else :
#            histprofNoTraffic.DrawCopy("SAMEHIST")
#        histprofNoTraffic.DrawCopy("SAMEHISTL][")

 #   upperPad.cd()
    leg.Draw("SAME")

    # Draw some arrows
    lin = TLine(12*60*60, 45., 12*60*60, 130.)
    lin.SetLineStyle(2)
    lin.Draw("SAME")

    if direction == 'West' :
        arr = TArrow(12*60*60, 130., 12*60*60+12*60*60, 130., 2., ">")
        arr.SetLineStyle(2)
        arr.Draw("SAME")
    elif direction == 'East' :
        arr = TArrow(12*60*60, 130., 12*60*60-12*60*60, 130., 2., ">")
        arr.SetLineStyle(2)
        arr.Draw("SAME")


  #  can.Update()
    can.SaveAs(fileName)
   
if __name__ == '__main__' :

    # Weird offset. Empirically determined. Only interested in time, for plotting.
    da = TDatime(2015,04,16,6,00,00);
    gStyle.SetTimeOffset(da.Convert());
    gStyle.SetOptStat(0)
    gROOT.SetBatch()

    drawShortestTimeInTraffic(routeList=listOfRoutes, direction = 'West', fileName='/home/cvilela/public_html/CommutesWest.pdf')    

    drawShortestTimeInTraffic(routeList=listOfRoutes, direction = 'East', fileName='/home/cvilela/public_html/CommutesEast.pdf')    
