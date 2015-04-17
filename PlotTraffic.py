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
    upperPad = TPad("upperPad", "upperPad", 0., 0.5, 1., 1.)
    upperPad.SetBottomMargin(1e-6)


    upperPad.Draw()
    upperPad.SetGridy()
    lowerPad = TPad("lowerPad", "lowerPad", 0., 0., 1., 0.5)
    lowerPad.SetTopMargin(1e-6)
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
        histoDiff      = TH1D(ttreeName+'_histDiff', ttreeName, 36, 0, 24*60*60)
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

        histoDiff.Add(histprof)
        histprofNoTraffic = histoNoTraffic.ProfileX()
        histoDiff.Add(histprofNoTraffic, -1)

        histoDiff.SetLineColor(route[3])
        histoDiff.SetMarkerSize(0)
        
        if isFirst :
            isFirst=False
            histprof.GetXaxis().SetTimeDisplay(1);
            histprof.GetXaxis().SetTimeFormat("%H:%M");        
            histoDiff.GetXaxis().SetTimeDisplay(1);
            histoDiff.GetXaxis().SetTimeFormat("%H:%M");        
            histprof.SetMinimum(45.)
            histprof.SetMaximum(160.)
            histprof.SetTitle("Commute "+route[4]+";Time of departure;Duration in Traffic [minutes]")
            histoDiff.SetMinimum(0.)
            histoDiff.SetMaximum(59.9)
            histoDiff.SetTitle("Extra time due to traffic "+route[4]+";Time of departure;#Delta_{t} [minutes]")
            upperPad.cd()
            leg.AddEntry(histprof.DrawCopy("E1X0"), route[0], "l")
            lowerPad.cd()
            histoDiff.DrawCopy("E1X0")
            print 'Drawing first', ttreeName
        else :
            print 'Drawing SAME', ttreeName
            upperPad.cd()
            leg.AddEntry(histprof.DrawCopy("SAMEE1X0"), route[0], "l")
            lowerPad.cd()
            histoDiff.DrawCopy("SAMEE1X0")
        upperPad.cd()
        histprof.DrawCopy("SAMEHISTL][")
        lowerPad.cd()
        histoDiff.DrawCopy("SAMEHISTL][")
        

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
    upperPad.cd()
    leg.Draw("SAME")

    # Draw some arrows
    lin = TLine(12*60*60, 45., 12*60*60, 130.)
    lin.SetLineStyle(2)
    lin.SetLineColor(632)
    lin.Draw("SAME")

    if direction == 'West' :
        arr = TArrow(12*60*60, 130., 12*60*60+12*60*60, 130., 2., ">")
        arr.SetLineStyle(2)
        arr.SetLineColor(632)
        arr.Draw("SAME")
    elif direction == 'East' :
        arr = TArrow(12*60*60, 130., 12*60*60-12*60*60, 130., 2., ">")
        arr.SetLineStyle(2)
        arr.SetLineColor(632)
        arr.Draw("SAME")
    lowerPad.cd()
    lin2 = TLine(12*60*60, 0., 12*60*60, 59.9)
    lin2.SetLineStyle(2)
    lin2.SetLineColor(632)
    lin2.Draw("SAME") 


  #  can.Update()
    can.SaveAs(fileName)
   
if __name__ == '__main__' :

    # Weird offset. Empirically determined. Only interested in time, for plotting.
    da = TDatime(2015,04,16,6,00,00);
    gStyle.SetTimeOffset(da.Convert());
    gStyle.SetOptStat(0)
    gStyle.SetTitleX(0.2)
    gROOT.SetBatch()

    drawShortestTimeInTraffic(routeList=listOfRoutes, direction = 'West', fileName='/home/cvilela/public_html/CommutesWest.pdf')    

    drawShortestTimeInTraffic(routeList=listOfRoutes, direction = 'East', fileName='/home/cvilela/public_html/CommutesEast.pdf')    
