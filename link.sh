#!/bin/sh

# FIXME: readlink -f does not work on macOS
SOURCE_DIR=`dirname "$(readlink -f "$0")"`
cd ~ 
ln -is "$SOURCE_DIR/slicerrc.py" ".slicerrc.py"

