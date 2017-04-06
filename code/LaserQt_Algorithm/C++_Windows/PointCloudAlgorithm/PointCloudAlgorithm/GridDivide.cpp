//#include "stdafx.h"
#include "GridDivide.h"
#include <iostream>

griddivide::griddivide(double* M, const int32_t M_num, const int32_t dim)
	: min_x(DBL_MAX), max_x(DBL_MIN), min_y(DBL_MAX), 
	  max_y(DBL_MIN), min_z(DBL_MAX), max_z(DBL_MIN)
{
	for(int i=0; i<M_num; i++)
	{
		if(min_x > M[i*dim + 0])
			min_x = M[i*dim + 0];
		if(min_y > M[i*dim + 1])
			min_y = M[i*dim + 1];
		if(min_z > M[i*dim + 2])
			min_z = M[i*dim + 2];
		if(max_x < M[i*dim + 0])
			max_x = M[i*dim + 0];
		if(max_y < M[i*dim + 1])
			max_y = M[i*dim + 1];
		if(max_z < M[i*dim + 2])
			max_z = M[i*dim + 2];
	}
}

void griddivide::grid_point(double *M, const int32_t M_num, const int32_t dim)
{
	double interval_x = (max_x - min_x)/(n_x-1);
	double interval_y = (max_y - min_y)/(n_y-1);
	double interval_z = (max_z - min_z)/(n_z-1);

	for(int i=0; i<M_num; i++) {
		double x = M[i*dim + 0];
		double y = M[i*dim + 1];
		double z = M[i*dim + 2];

		// 三维空间长a、宽b、高c的坐标表示为a+b*nx+c*nx*ny
		int grid_x = ((int)((x - min_x) / interval_x));
		int grid_y = ((int)((y - min_y) / interval_y));
		int grid_z = ((int)((z - min_z) / interval_z));
		int size = point.size();
		Pointxyz.push_back(Point_xyz(x, y, z, grid_x, grid_y, grid_z, size));
		point[grid_x + grid_y * n_x + grid_z * n_x * n_y].push_back(i);
	}
}

void griddivide::grid_fitcurve(double * M, vector<int>& p, 
	double threshold, int pos, const int dim)
{
	// 获取法向量
	double* T = new double[p.size() * 3];
	for (int i = 0; i < p.size(); ++i) {
		T[i * dim + 0] = M[p[i] * dim + 0];
		T[i * dim + 1] = M[p[i] * dim + 1];
		T[i * dim + 2] = M[p[i] * dim + 2];
	}
	IcpPointToPlane icp(T, p.size(), dim, 5);
	double *M_normal = icp.getM_normal();

	// 获取平均点
	int grid_z = pos / (n_x*n_y);
	int grid_y = (pos % (n_x*n_y)) / n_x;
	int grid_x = (pos % (n_x*n_y)) % n_x;
	int len = p.size();
	Point_xyz P_aver(0, 0, 0, grid_x, grid_y, grid_z, -1);
	for (int i = 0; i < p.size(); ++i) {
		P_aver.x += M[p[i] * dim + 0];
		P_aver.y += M[p[i] * dim + 1];
		P_aver.z += M[p[i] * dim + 2];
	}
	P_aver.x = P_aver.x / len;
	P_aver.y = P_aver.y / len;
	P_aver.z = P_aver.z / len;

	// 求所有点到平均点的距离及该点的权重和总法向量
	vector<double> dist(p.size(), 0), w(p.size(), 0);
	double max_dist = 0;
	vector<double> N(3, 0);
	for (int i = 0; i < p.size(); ++i) {
		double temp = sqrt(pow((M[p[i] * dim + 0] - P_aver.x), 2) +
			pow((M[p[i] * dim + 1] - P_aver.y), 2) + pow((M[p[i] * dim + 2] - P_aver.z), 2));
		dist[i] = temp;
		if (temp > max_dist)
			max_dist = temp;
	}
	for (int i = 0; i < p.size(); ++i) {
		w[i] = (1 - dist[i] / max_dist) + 0.2; // 人为定义的权重
		N[0] += M_normal[i * dim + 0] * w[i] / p.size();
		N[1] += M_normal[i * dim + 1] * w[i] / p.size();
		N[2] += M_normal[i * dim + 2] * w[i] / p.size();
	}
	vector<double> p_aver(3, 0);
	p_aver[0] = P_aver.x;
	p_aver[1] = P_aver.y;
	p_aver[2] = P_aver.z;
	N = DivideVector(N, norm_p(N));
	vector<double> D = cross_product(p_aver, N);

	// 重新修正坐标点，以P_aver为原点，总法向量为z轴
	double *M_new = new double[p.size() * 3];
	for (int i = 0; i < p.size(); ++i) {
		vector<double> P_j(3, 0), N_j(3, 0), P_n(3, 0);
		P_j[0] = M[p[i] * dim + 0];
		P_j[1] = M[p[i] * dim + 1];
		P_j[2] = M[p[i] * dim + 2];
		//N_j[0] = M_normal[i * dim + 0];
		//N_j[1] = M_normal[i * dim + 1];
		//N_j[2] = M_normal[i * dim + 2];

		//// 求网格点到微平面的有向距离
		//vector<double> d_n = AddVector(D, dot_product(N_j, P_j));
		//P_n = SubVector(P_j, cross_product(d_n, N));
		//vector<double> u = DivideVector(P_n, norm_p(P_n));
		//vector<double> v = cross_product(N, u);
		//M_new[i * dim + 0] = dot_product(P_n, u);
		//M_new[i * dim + 1] = dot_product(P_n, v);
		//M_new[i * dim + 2] = norm_p(d_n);
		
		double d_n = dot_product(N, SubVector(P_j, p_aver));
		P_n = SubVector(SubVector(P_j, p_aver), cross_product(N, abs(d_n)));
		M_new[i * dim + 0] = P_n[0];
		M_new[i * dim + 1] = P_n[1];
		M_new[i * dim + 2] = d_n;
	}

	// 令曲面方程为S = ax^2 + bxy + cy^2, 误差函数h = ax^2 + bxy + cy^2 - S
	// 误差平方和E = sum(h^2), 
	Matrix A(3, 3), b(3, 1);
	// E对a求偏导
	A.val[0][0] = SumVector(M_new, 4, 0, 0, p.size(), dim);
	A.val[0][1] = SumVector(M_new, 3, 1, 0, p.size(), dim);
	A.val[0][2] = SumVector(M_new, 2, 2, 0, p.size(), dim);
	b.val[0][0] = SumVector(M_new, 2, 0, 1, p.size(), dim);
	// E对b求偏导
	A.val[1][0] = SumVector(M_new, 3, 1, 0, p.size(), dim);
	A.val[1][1] = SumVector(M_new, 2, 2, 0, p.size(), dim);
	A.val[1][2] = SumVector(M_new, 1, 3, 0, p.size(), dim);
	b.val[1][0] = SumVector(M_new, 1, 1, 1, p.size(), dim);
	// E对c求偏导
	A.val[2][0] = SumVector(M_new, 2, 2, 0, p.size(), dim);
	A.val[2][1] = SumVector(M_new, 1, 3, 0, p.size(), dim);
	A.val[2][2] = SumVector(M_new, 0, 4, 0, p.size(), dim);
	b.val[2][0] = SumVector(M_new, 0, 2, 1, p.size(), dim);
	// 求解a,b,c的值
	b.solve(A);

	// 给定阈值进行滤波
	int x = b.val[0][0], y = b.val[1][0], z = b.val[2][0];
	for (int i = 0; i < p.size(); ++i) {
		double t = x * pow(M_new[i * dim + 0], 2) + y * M_new[i * dim + 0] * M_new[i * dim + 1]
			+ z * pow(M_new[i * dim + 1], 2) - M_new[i * dim + 2];
		if (abs(t) > threshold)
			M[p[i] * dim + 2] = NAN;
	}

	delete[] M_new;
}

double* griddivide::first_filter_grid(double* M, int& num_G, int dim, double threshold)
{
	for(int i=0; i<(int)point.size(); i++)
	{
		if (point[i].empty()) continue;
		if (point[i].size() && point[i].size() < 5) {
			ClearArray(M, point[i], dim);
			point[i].clear();	//	去除第一类噪声点
		}
		else {	// 如果网格内数据量比较多的话，就进行阈值筛选
			grid_fitcurve(M, point[i], threshold, i, dim);
		}
	}
	vector<int> temp_p(point.size(),0);

	int l=label_pointcloud(point, temp_p);	//	给点云数据进行标记
	vector<int> label_num(l, 0);
	for(int i=0; i<n_x; i++){
		for(int j=0; j<n_y; j++){
			for(int k=0; k<n_z; k++)
			{
				if(temp_p[i+j*n_x+k*n_x*n_y]>0)
					label_num[temp_p[i+j*n_x+k*n_x*n_y]-1]++;
			}
		}
	}
	int kk = 0;
	for (int i = 1; i < l; i++) {
		if (label_num[i] > label_num[kk])
			kk = i;
	}

	vector<double> tmp;	//	临时存放数据
	for(int i=0; i<n_x; i++){
		for(int j=0; j<n_y; j++){
			for(int k=0; k<n_z; k++)
			{
				if (temp_p[i + j*n_x + k*n_x*n_y] != kk + 1) {
					ClearArray(M, point[i + j*n_x + k*n_x*n_y], dim);
					point[i + j*n_x + k*n_x*n_y].clear();
				}
					
			}
		}
	}
	
	//	还需要其他的滤波措施，所以与清除第二类噪声点分开
	for(int i=0; i<n_x; i++){
		for(int j=0; j<n_y; j++){
			for(int k=0; k<n_z; k++) {
				for(int a=0; a<point[i+j*n_x+k*n_x*n_y].size(); a++) {
					tmp.push_back(M[point[i+j*n_x+k*n_x*n_y][a]*dim+0]);
					tmp.push_back(M[point[i+j*n_x+k*n_x*n_y][a]*dim+1]);
					tmp.push_back(M[point[i+j*n_x+k*n_x*n_y][a]*dim+2]);
					num_G++;
				}
			}
		}
	}
	double* res=new double[tmp.size()];
	for(int i=0; i<tmp.size(); i++)
		res[i]=tmp[i];

	return res;
}

int griddivide::label_pointcloud(vector<vector<int>>& point, vector<int>& temp)
{
	int label=0;
	queue<int> point_temp;
	vector<bool> hasvisited(temp.size(),false);
	for(int i=0; i<n_x; i++){
		for(int j=0; j<n_y; j++){
			for(int k=0; k<n_z; k++)
			{
				int pos=i+j*n_x+k*n_x*n_y;
				if(point[pos].size()&&temp[pos]==0&&hasvisited[pos]==false)
				{
					point_temp.push(pos);
					label++;
					temp[i+j*n_x+k*n_x*n_y]=label;
					label_point(point, temp, i, j, k, point_temp);
				}
			}
		}
	}
	return label; 
}

void griddivide::label_point(vector<vector<int>> point, vector<int>& temp, int i, int j, int k, queue<int>& point_temp)
{
	// 创建队列，将访问到的点存入队列
	while (point_temp.size()) {
		int pos=point_temp.front();
		point_temp.pop();
	
		int label = temp[i + j*n_x + k*n_x*n_y];
		for (int x = i - 1; x <= i + 1; x++) {
			for (int y = j - 1; y <= j + 1; y++) {
				for (int z = k - 1; z <= k + 1; z++)
				{
					if (x < 0 || x >= n_x || y < 0 || y >= n_y || z < 0 || z >= n_z)
						continue;
					if (point[x + y*n_x + z*n_x*n_y].size() && temp[x + y*n_x + z*n_x*n_y] == 0)
					{
						temp[x + y*n_x + z*n_x*n_y] = label;
						point_temp.push(x + y*n_x + z*n_x*n_y);
					}
				}
			}
		}
		int z = pos / (n_x*n_y);
		int y = (pos % (n_x*n_y)) / n_x;
		int x = (pos % (n_x*n_y)) % n_x;
		label_point(point, temp, x, y, z, point_temp);
	}
}

// 向量点乘
double dot_product(vector<double> x, vector<double> y)
{
	if (x.size() != 3 || y.size() != 3) return 0;
	return x[0] * y[0] + x[1] * y[1] + x[2] * y[2];
}
// 向量叉乘
vector<double> cross_product(vector<double> x, vector<double> y)
{
	vector<double> res(3, 0);
	if (x.size() != 3 || y.size() != 3) return res;
	res[0] = x[1] * y[2] - y[1] * x[2];
	res[1] = x[2] * y[0] - y[2] * x[0];
	res[2] = x[0] * y[1] - y[0] * x[1];
	return res;
}
// 向量模
double norm_p(vector<double> v)
{
	if (v.size() != 3) return 0;
	return sqrt(pow(v[0], 2) + pow(v[1], 2) + pow(v[2], 2));
}
// 向量加法
vector<double> AddVector(vector<double> v, double num)
{
	vector<double> res = v;
	res[0] += num;
	res[1] += num;
	res[2] += num;
	return res;
}
// 向量减法
vector<double> SubVector(vector<double> v1, vector<double> v2)
{
	vector<double> res = v1;
	res[0] -= v2[0];
	res[1] -= v2[1];
	res[2] -= v2[2];
	return res;
}
// 向量除法
vector<double> DivideVector(vector<double> v, double num)
{
	vector<double> res = v;
	if (num == 0) { res.clear(); return res; }
	res[0] /= num;
	res[1] /= num;
	res[2] /= num;
	return res;
}
// 求和平均值
double SumVector(double *M, int i, int j, int k, int N, int dim)
{
	double res = 0;
	for (int a = 0; a < N; ++a)
		res += pow(M[a * dim + 0], i) * pow(M[a * dim + 1], j) * pow(M[a * dim + 2], k);
	res /= N;
	return res;
}
vector<double> cross_product(vector<double> v, double n)
{
	vector<double> res = v;
	res[0] *= n;
	res[1] *= n;
	res[2] *= n;
	return res;
}
// 将清除掉的点到原数组中赋NaN
void ClearArray(double *M, vector<int> p, int dim)
{
	for (auto c : p)
		M[c * dim + 2] = NAN;
}
// 获取z向间隔作为阈值
double griddivide::GetInterval()
{
	return (max_z - min_z) / (n_z - 1);
}