#ifndef READFILE_H
#define READFILE_H

#pragma warning(disable:4996)

#include <fstream>
#include <vector>
#include "matrix.h"

extern "C" __declspec(dllexport) double* ReadFile(char* strPath, int32_t& num, int32_t& dim);
extern "C" __declspec(dllexport) void WriteFile(char* Path, double* M, int32_t num, int32_t dim);

#endif