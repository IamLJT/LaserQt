#ifndef FILTER_H
#define FILTER_H

#include "matrix.h"

class Filter
{
public:
	Filter(double *M, const int32_t M_num, const int32_t dim):M(M),M_num(M_num),dim(dim){};

	double GetMedian(Matrix mx, int row, int col);
	double* SimpleFilter();		//	For shot noise ¡ª¡ª Medium Filter or Mesh Denoise

	//	For Scantterd Noise
	void FurtherFilter();

protected:
	double* M;				//	source data
	int32_t M_num;			//	number of data
	const int32_t dim;		//	dimension
};

#endif