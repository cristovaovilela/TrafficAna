#!/usr/bin/python

import sys
import os.path
import urllib2
import numpy
import re
import datetime
from array import array
from subprocess import call

from ROOT import TFile, TTree, gROOT

def getDataFillTTree( ttreeName, start, end  ):

  # Fetch google directions
  data = urllib2.urlopen('https://www.google.com/maps/dir/'+start+'/'+end)
  dataString = data.read()
  
  # Check the time
  nowTime = datetime.datetime.now()
  
  # Get routes
  routeList = routeP.findall(dataString)
  
  # Open ROOT file and TTree
  #  rootFile = TFile(ttreeName+'.root', 'update')
  # Dirty hack to avoid TTree duplicates
  rootFile = TFile('temp.root', 'RECREATE')

  # Set up TTree variables
  year = numpy.zeros(1, dtype=int)
  month = numpy.zeros(1, dtype=int)
  day = numpy.zeros(1, dtype=int)
  hour = numpy.zeros(1, dtype=int)
  minute = numpy.zeros(1, dtype=int)
  weekday = numpy.zeros(1, dtype=int)

  distance = numpy.zeros(1, dtype=float)
  timeNoTraffic = numpy.zeros(1, dtype=int)
  timeInTraffic = numpy.zeros(1, dtype=int)

  routeName = array('c', 'aRoute\0')
  
  # Check if TTree exists and set it up
  # No need for dirty trick
  #  rootTTree = rootFile.Get(ttreeName)

# Same
#  if not rootTTree :
#    print 'TTree not found'
  rootTTree = TTree(ttreeName, ttreeName)
  
  rootTTree.Branch('year', year, 'year/I')
  rootTTree.Branch('month', month, 'month/I')
  rootTTree.Branch('day', day, 'day/I')
  rootTTree.Branch('hour', hour, 'hour/I')
  rootTTree.Branch('minute', minute, 'minute/I')
  rootTTree.Branch('weekday', weekday, 'weekday/I')
  
  rootTTree.Branch('distance', distance, 'distance/D')
  rootTTree.Branch('timeNoTraffic', timeNoTraffic, 'timeNoTraffic/I')
  rootTTree.Branch('timeInTraffic', timeInTraffic, 'timeInTraffic/I')
  rootTTree.Branch('routeName', routeName, 'routeName/C')
  
  # Fill TTree
  year[0] = nowTime.year
  month[0] = nowTime.month
  day[0] = nowTime.day
  hour[0] = nowTime.hour
  minute[0] = nowTime.minute
  weekday[0] = nowTime.weekday()
  
  for route in routeList :
    distance[0] = parseDistance(route[0])
    timeNoTraffic[0] = parseTime(route[1])
    timeInTraffic[0] = parseTime(route[2])
    routeName = array('c', route[3]+'\0')
    rootTTree.SetBranchAddress('routeName', routeName)
    rootTTree.Fill()

  # Close File
  rootFile.Write()
  rootFile.Close()
  
  # Dirty trick c'ed
  if not os.path.isfile(ttreeName+".root") :
    call(["mv", "temp.root", ttreeName+".root"])
  else :
    call(["hadd", "summed.root", ttreeName+".root", "temp.root"])
    call(["mv", "summed.root", ttreeName+".root"])
    call(["rm", "temp.root"])

def parseTime( timeString ) :
  
  hourMinList = hourMinP.findall( timeString )

  if len(hourMinList) :
    return int(hourMinList[0][0])*60+int(hourMinList[0][1])
  else :
    minList = minP.findall(timeString)
    return int(minList[0])

def parseDistance( distanceString ) :
  noMilesList = noMilesP.findall( distanceString )
  return float(noMilesList[0])


if __name__ == '__main__' :

  # Sort out regular expressions only once
  global routeP, hourMinP, minP, noMilesP
  
  routePattern = '<li class="dir-altroute" id="altroute_." altid="." oi="alt_.".*?<div class="altroute-rcol altroute-info">.*?<span>(?P<distance>.*?)</span>,.*?<span>(?P<timeNoTraffic>.*?)</span>.*?</div>.*?<div class="altroute-rcol altroute-aux">.*?<span>.*?In current traffic:(?P<timeInTraffic>.*?)</span>.*?</div>.*?<div>(?P<routeName>.*?)</div>.*?<div class="dir-altroute-clear">.*?</div>.*?</div>.*?</li>'
  routeP = re.compile(routePattern)
  
  hourMinPattern = '\s*(?P<hours>\d*)\s*hour.\s*(?P<minutes>\d*)\s*min.*\s*'
  hourMinP = re.compile(hourMinPattern)

  minPattern = '\s*(?P<minutes>\d*)\s*min.*\s*'
  minP = re.compile(minPattern)
    
  noMilesPattern = '\s*(?P<distance>[^mi\s]*).*'
  noMilesP = re.compile(noMilesPattern)


  # Define the list of routes to probe
  # Coordinates for Stony Brook Physics parking lot
  StonyBrook = '40.9145565,-73.1271978'


  # Morningside / Harlem / East Harlem
  # ====================
  # Amsterdam and 23rd
  Ams23rd = "Amsterdam+Ave+%26+W+123rd+St,+New+York,+NY+10027"
  # Adam Clayton and W 116th
  Adm116th = "Adam+Clayton+Powell+Jr+Blvd+%26+W+116th+St,+New+York,+NY+10026"
  # 3rd Avenue and E 111th
  Third111th = "3rd+Ave+%26+E+111th+St,+New+York,+NY+10029"
  # Lexington and E 103
  Lex103rd = "Lexington+Ave+%26+E+103rd+St,+New+York,+NY+10029"

  # Astoria
  # ====================
  # Broadway and Crescent
  BroCre = "Broadway+%26+Crescent+St,+Astoria,+NY+11106"
  # Broadway and Newtown rd
  BroNew = "Broadway+%26+Newtown+Rd,+Queens,+NY+11377"
  
  # Jackson Heights
  # ====================
  # 32nd Ave and 80th
  ThirtySecond80th = "32nd+Ave+%26+80th+St,+East+Elmhurst,+NY+11370"

  # Woodside
  # ====================
  Roo63rd = "Roosevelt+Ave+%26+63rd+St,+Woodside,+NY+11377"
  
  # Elmhurst
  # ====================
  Woo77th = "Woodside+Ave+%26+77th+St,+Elmhurst,+NY+11373"
  
  # Corona
  # ====================
  RooJun = "Roosevelt+Ave+%26+Junction+Blvd,+Queens,+NY+11368"

  # Forest Hills
  # ====================
  AusCont = "Austin+St+%26+Continental+Ave,+Forest+Hills,+NY+11375"

  listOfRoutes = [ ["MorningsideToSBU",     Ams23rd,           StonyBrook      ],
                   ["SBUToMorningside",     StonyBrook,        Ams23rd         ],
                   ["HarlemToSBU",          Adm116th,          StonyBrook      ],
                   ["SBUToHarlem",          StonyBrook,        Adm116th        ],
                   ["EastHarlemToSBU",      Third111th,        StonyBrook      ],
                   ["SBUTpEastHarlem",      StonyBrook,        Third111th      ],
                   ["YorkvilleToSBU",       Lex103rd,          StonyBrook      ],
                   ["SBUToYorkville",       StonyBrook,        Lex103rd        ],
                   ["Astoria1ToSBU",        BroCre,            StonyBrook      ],
                   ["SBUToAstoria1",        StonyBrook,        BroCre          ],
                   ["Astoria2ToSBU",        BroNew,            StonyBrook      ],
                   ["SBUToAstoria2",        StonyBrook,        BroNew          ],
                   ["JackToSBU",            ThirtySecond80th,  StonyBrook      ],
                   ["SBUToJack",            StonyBrook,        ThirtySecond80th], 
                   ["WoodsideToSBU",        Roo63rd,           StonyBrook      ],
                   ["SBUToWoodside",        StonyBrook,        Roo63rd         ],
                   ["ElmhurstToSBU",        Woo77th,           StonyBrook      ],
                   ["SBUToElmhurst",        StonyBrook,        Woo77th         ],
                   ["CoronaToSBU",          RooJun,            StonyBrook      ],
                   ["SBUToCorona",          StonyBrook,        RooJun          ],
                   ["ForestHillsToSBU",     AusCont,           StonyBrook      ],
                   ["SBUToForestHills",     StonyBrook,        AusCont         ] ]
                   

  for route in listOfRoutes :
    getDataFillTTree( ttreeName = route[0], start = route[1], end = route[2] )

