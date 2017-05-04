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
	
	double GetMax_z() { return max_z; }
	double GetMin_z() { return min_z; }
	void grid_point(double *M, const int32_t M_num, const int32_t dim);

	double* first_filter_grid(double* M, int& num_G, int dim, double threshold);
	int label_pointcloud(vector<vector<int>>& point, vector<int>& temp);
	void label_point(vector<vector<int>> point, vector<int>& temp, int x, int y, int z, queue<int>& point_temp);
	void grid_fitcurve(double * M, vector<int>& p, double threshold, int pos, const int dim);
	double GetInterval();
	double* gridconvert(double* M, int& num, double* M_c);	// 转换成图像数据
	//double* griddivide::RotateImage(double* M, int num);	// 旋转图像

private:
	double min_x, max_x;
	double min_y, max_y;
	double min_z, max_z;

	int n_x, n_y, n_z, dim, num;
	vector<vector<int>> point;
	vector<Point_xyz> Pointxyz;
};

Matrix fit_plane(double* M, int dim, int num);

double dot_product(vector<double> x, vector<double> y);
vector<double> cross_product(vector<double> x, vector<double> y);
vector<double> cross_product(vector<double> v, double n);

vector<double> AddVector(vector<double> v, double num);
vector<double> SubVector(vector<double> v1, vector<double> v2);
vector<double> DivideVector(vector<double> v, double num);
double SumVector(double *M, int i, int j, int k, int N, int dim);
double norm_p(vector<double> v);
void ClearArray(double *M, vector<int> p, int dim);

int GetIndexOfKmeans(vector<vector<double>> Kmeans, double* M, int index, int dim);
double* RotateImage(double* M, int num, int dim, int mode = 1);	// 旋转图像


// 2017/04/20新的网格分割和聚类
class griddivide_new {
public:
	griddivide_new(double* M, const int32_t M_num, const int32_t dim);
	void gridpoint(double* M, double cubsize);
	double* grid_filter(double* M, int& count, int min_p, int mode = 1);
	vector<vector<double>> grid_kmeans(double* M, int k, int num);

private:
	double min_x, max_x;
	double min_y, max_y;
	double min_z, max_z; // 最大点和最小点坐标
	int n_x, n_y, n_z;
	const int num, dim;
	vector<vector<int>> point;
	vector<vector<double>> P_new;
	// point记录网格内的点，P_new记录新的点云点（跟网格数相同）

};

#endif