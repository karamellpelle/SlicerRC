#!/bin/sh

SOURCE_DIR=`dirname "$(readlink -f "$0")"`
cd ~ 
ln -is "$SOURCE_DIR/slicerrc.py" ".slicerrc.py"

