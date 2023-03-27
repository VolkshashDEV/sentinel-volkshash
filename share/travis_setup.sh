#!/bin/bash
set -evx

mkdir ~/.volkshashcore

# safety check
if [ ! -f ~/.volkshashcore/.volkshash.conf ]; then
  cp share/volkshash.conf.example ~/.volkshashcore/volkshash.conf
fi
