#ifndef __GRIDDIVIDE_H_
#define __GRIDDIVIDE_H_

#include "matrix.h"
#include <vector>
#include <algorithm>
#include <queue>

using namespace std;

class griddivide{

public:
	griddivide(double *M, const int32_t M_num, const int32_t dim);
	void dividenum(int nx, int ny, int nz)
	{
		n_x=nx, n_y=ny, n_z=nz;
		point.resize(n_x*n_y*n_z);
	}

	void grid_point(double *M, const int32_t M_num, const int32_t dim);

	double* first_filter_grid(double* M, int& num_G, int dim);
	int label_pointcloud(vector<vector<int>>& point, vector<int>& temp);
	void label_point(vector<vector<int>> point, vector<int>& temp, int x, int y, int z, queue<int>& point_temp);

private:
	double min_x, max_x;
	double min_y, max_y;
	double min_z, max_z;

	int n_x, n_y, n_z;
	vector<vector<int>> point;
};

#endif