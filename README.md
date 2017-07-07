# IDOLProtocolClassifier
Second version of IDOL protocol packets classifier.

# Requirements:
Requirements:

  - python version 2 (tested on 2.7)
  - swig utility
  - scapy module for python
  - json module for python
  - sudo access

# How to start? 
Start guide:

  - To install program run command:
           $ ./install.sh
           
    It will install & translate C functions into python module. 
    This module is required by idol.py.
    If instalation breaks, follow instructions printed to terminal.

# How to run?
Run guide:

  - To run this program you need to execute command:
           $ sudo python idol.py [*.json] [*.txt]
           
    * sudo    - required, because program need to work with sockets
    * python  - you need to have python version 2
    * idol.py - current program
    * .json  - if you have custom receivers file, you can use it
    * .txt   - if you have another logs file, you are able to use it
    
