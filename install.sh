#!/bin/bash

swig -python fileloader.i 2>/dev/null || \
           { echo -e >&2 '\n Swig utility required. To install use :\n'\
                         ' $ sudo apt-get install swig \n' ; exit 1; }

python setup.py build_ext --inplace 2>/dev/null || \
           { echo -e >&2 '\n Python v2.7 required. To install use :\n'\
                         ' $ sudo apt-get install python \n' ; exit 1; }

echo -e '\n Sucessfull files generation. Next command :'\
        '\n $ sudo python idol.py [*.json] [*.txt]\n'

