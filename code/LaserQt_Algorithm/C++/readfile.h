#ifndef __READFILE_H__
#define __READFILE_H__

#pragma warning(disable:4996)

#include <fstream>
#include <vector>
#include "matrix.h"

double* ReadFile(const char* strPath, std::vector<int>& DataFile);
void WriteFile(char* Path, double* M, int32_t num, int32_t dim);

#endif  // __READFILE_H__