#include "fileloader.h"
#include <stdio.h>
#include <stdlib.h>

const char* get_file_content(const char* path)
{
    int length;
    FILE* file = fopen(path, "r");
    char* content;    
    fseek(file, 0, SEEK_END);
    length = ftell(file);
    fseek(file, 0, SEEK_SET);
    content = malloc(length);
    if(content)
    {
      fread(content, 1, length, file);
    }
    fclose(file);

    return content;
}
