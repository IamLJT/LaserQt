#ifndef FILTER_H
#define FILTER_H

#include "matrix.h"

class Filter
{
public:
	Filter(double *M, const int32_t M_num, const int32_t dim, int m, int n);

	void copyData(double *M, int dim, int m, int n);

	double GetChordHeight(Matrix mx, bool direc, int row, int col);	//	获取弦高
	double GetMedian(Matrix mx, int w_core, int row, int col);		//	获取算子的中值
	double GetMean(Matrix mx, int w_core, int row, int col);		//	获取算子的均值
	double GetBFilter2(Matrix mx, int w_core, int row, int col, int sigma_s, int sigma_r);	//	获取算子的双边滤波值

	double* ThresholdFilter(double threshold = 20);	//	define a threshold, and find the noise number.
	double* SimpleFilter();		//	For shot noise —— Medium Filter or Mesh Denoise.

	//	For Scantterd Noise
	double* bFilter2();
	double* FurtherFilter();

public:
	int noisenum;
	Matrix mx;
	double* M;				//	source data
	int32_t M_num;			//	number of data
	const int32_t dim;		//	dimension
	int m, n;				//	row and col of matrix
};

#endif