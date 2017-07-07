#!/usr/bin/env python
"""
File reading module for idol.py.

Module used to generate from C sources files Python module.

Require : python
Syntax of run command :
$ python <name_of_program>


"""
from distutils.core import setup, Extension

fileloader_module = Extension('_fileloader',
                              sources=['fileloader_wrap.c', 'fileloader.c'])

setup(name='fileloader', 
      ext_modules=[fileloader_module], 
      py_modules=['fileloader'])
