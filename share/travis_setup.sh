#!/bin/bash
set -evx

mkdir ~/.dtmicore

# safety check
if [ ! -f ~/.dtmicore/.dtmi.conf ]; then
  cp share/dtmi.conf.example ~/.dtmicore/dtmi.conf
fi
