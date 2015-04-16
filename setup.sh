#!/bin/bash

# Setup ROOT and Geant4 from the ND280 install
export CMTPATH=/home/t2k/ND280_Software/GLOBAL-nd280Tools-versioned/v1r43
source /home/t2k/ND280_Software/GLOBAL-nd280Tools-versioned/v1r43/ROOT/v5r34p01n02/cmt/setup.sh

export LD_LIBRARY_PATH=$ROOTSYS/lib:$PYTHONDIR/lib:$LD_LIBRARY_PATH
export PYTHONPATH=$ROOTSYS/lib:$PYTHONPATH

