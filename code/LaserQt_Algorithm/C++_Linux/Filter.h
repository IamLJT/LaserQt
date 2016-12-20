#ifndef FILTER_H
#define FILTER_H

#include "matrix.h"

class Filter
{
public:
	Filter(double *M, const int32_t M_num, const int32_t dim, int m, int n);

	double GetMedian(Matrix mx, int w_core, int row, int col);
	double GetMean(Matrix mx, int w_core, int row, int col);
	double GetBFilter2(Matrix mx, int w_core, int row, int col, int sigma_s, int sigma_r);

	double* SimpleFilter();		//	For shot noise ¡ª¡ª Medium Filter or Mesh Denoise

	//	For Scantterd Noise
	double* bFilter2();
	double* FurtherFilter();

protected:
	Matrix mx;
	double* M;				//	source data
	int32_t M_num;			//	number of data
	const int32_t dim;		//	dimension
	int m, n;				//	row and col of matrix
};

#endif