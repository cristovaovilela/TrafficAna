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

# LIE HOV lanes
# ====================
hovWgoingE = "40.762898,-73.727901"
hovWgoingW = "40.762965,-73.728028"

hovEgoingE = "40.818578,-73.061615"
hovEgoingW = "40.819116,-73.061706"

listOfRoutes = [ ["MorningsideToSBU",     Ams23rd,           StonyBrook       , 840   , 'East'],
                 ["SBUToMorningside",     StonyBrook,        Ams23rd          , 840   , 'West'],
                 ["HarlemToSBU",          Adm116th,          StonyBrook       , 600   , 'East'],
                 ["SBUToHarlem",          StonyBrook,        Adm116th         , 600   , 'West'],
                 ["EastHarlemToSBU",      Third111th,        StonyBrook       , 594   , 'East'],
                 ["SBUTpEastHarlem",      StonyBrook,        Third111th       , 594   , 'West'],
                 ["YorkvilleToSBU",       Lex103rd,          StonyBrook       , 616   , 'East'],
                 ["SBUToYorkville",       StonyBrook,        Lex103rd         , 616   , 'West'],
                 ["Astoria1ToSBU",        BroCre,            StonyBrook       , 632   , 'East'],
                 ["SBUToAstoria1",        StonyBrook,        BroCre           , 632   , 'West'],
                 ["Astoria2ToSBU",        BroNew,            StonyBrook       , 629   , 'East'],
                 ["SBUToAstoria2",        StonyBrook,        BroNew           , 629   , 'West'],
                 ["JackToSBU",            ThirtySecond80th,  StonyBrook       , 420   , 'East'],
                 ["SBUToJack",            StonyBrook,        ThirtySecond80th , 420   , 'West'], 
                 ["WoodsideToSBU",        Roo63rd,           StonyBrook       , 416   , 'East'],
                 ["SBUToWoodside",        StonyBrook,        Roo63rd          , 416   , 'West'],
                 ["ElmhurstToSBU",        Woo77th,           StonyBrook       , 414   , 'East'],
                 ["SBUToElmhurst",        StonyBrook,        Woo77th          , 414   , 'West'],
                 ["CoronaToSBU",          RooJun,            StonyBrook       , 807   , 'East'],
                 ["SBUToCorona",          StonyBrook,        RooJun           , 807   , 'West'],
                 ["ForestHillsToSBU",     AusCont,           StonyBrook       , 801   , 'East'],
                 ["SBUToForestHills",     StonyBrook,        AusCont          , 801   , 'West'],
                 ["LIE_HOV_East",         hovWgoingE,        hovEgoingE       , 1     , 'LIEE'],
                 ["LIE_HOV_West",         hovEgoingW,        hovWgoingW       , 1     , 'LIEW']]
