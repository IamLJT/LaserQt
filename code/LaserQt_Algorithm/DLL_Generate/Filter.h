#ifndef FILTER_H
#define FILTER_H

#include "matrix.h"

class Filter
{
public:
	Filter(double *M, const int32_t M_num, const int32_t dim, int m, int n);

	void copyData(double *M, int dim, int m, int n);

	double GetChordHeight(Matrix mx, bool direc, int row, int col);
	double GetMedian(Matrix mx, int w_core, int row, int col);
	double GetMean(Matrix mx, int w_core, int row, int col);
	double GetBFilter2(Matrix mx, int w_core, int row, int col, int sigma_s, int sigma_r);

	double* ThresholdFilter(double threshold = 20);	//	define a threshold, and find the noise number.
	double* SimpleFilter();		//	For shot noise ¡ª¡ª Medium Filter or Mesh Denoise.

	//	For Scantterd Noise
	double* bFilter2();
	double* FurtherFilter();

protected:
	int noisenum;
	Matrix mx;
	double* M;				//	source data
	int32_t M_num;			//	number of data
	const int32_t dim;		//	dimension
	int m, n;				//	row and col of matrix
};

#endif