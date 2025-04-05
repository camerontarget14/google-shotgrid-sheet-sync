#! /bin/sh

pex . -r requirements.txt -m baked_tools \
    --python-shebang='/usr/bin/env python3' \
    -o baked-tools.pex
