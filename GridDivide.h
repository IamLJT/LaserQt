#ifndef __GRIDDIVIDE_H_
#define __GRIDDIVIDE_H_

#include "matrix.h"
#include "icpPointToPlane.h"
#include <vector>
#include <algorithm>
#include <queue>

using namespace std;

struct Point_xyz {
	double x, y, z;
	int grid_x, grid_y, grid_z;
	int index;
public:
	Point_xyz() :
		x(-1), y(-1), z(-1), grid_x(-1), grid_y(-1),
		grid_z(-1), index(-1) {}
	Point_xyz(double x, double y, double z,
		int grid_x, int grid_y, int grid_z, int index) :
		x(x), y(y), z(z), grid_x(grid_x), grid_y(grid_y),
		grid_z(grid_z), index(index) {}
};

class griddivide{

public:
	griddivide(double *M, const int32_t M_num, const int32_t dim);
	void dividenum(int nx, int ny, int nz) {
		n_x = nx;
		n_y = ny;
		n_z = nz;
		point.resize(n_x*n_y*n_z);
	}

	void grid_point(double *M, const int32_t M_num, const int32_t dim);

	double* first_filter_grid(double* M, int& num_G, int dim, double threshold);
	int label_pointcloud(vector<vector<int>>& point, vector<int>& temp);
	void label_point(vector<vector<int>> point, vector<int>& temp, int x, int y, int z, queue<int>& point_temp);
	void grid_fitcurve(double * M, vector<int>& p, double threshold, int pos, const int dim);
	double GetInterval();

private:
	double min_x, max_x;
	double min_y, max_y;
	double min_z, max_z;

	int n_x, n_y, n_z;
	vector<vector<int>> point;
	vector<Point_xyz> Pointxyz;
};

double dot_product(vector<double> x, vector<double> y);
vector<double> cross_product(vector<double> x, vector<double> y);
vector<double> cross_product(vector<double> v, double n);

vector<double> AddVector(vector<double> v, double num);
vector<double> SubVector(vector<double> v1, vector<double> v2);
vector<double> DivideVector(vector<double> v, double num);
double SumVector(double *M, int i, int j, int k, int N, int dim);
double norm_p(vector<double> v);
void ClearArray(double *M, vector<int> p, int dim);

#endif