%module fileloader
%{
#define SWIG_FILE_WITH_INIT
#include "fileloader.h"
%}

const char* get_file_content(const char* path);
