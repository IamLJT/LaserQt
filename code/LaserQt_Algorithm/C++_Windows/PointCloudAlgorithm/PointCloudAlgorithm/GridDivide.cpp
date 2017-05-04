//#include "stdafx.h"
#include "GridDivide.h"
#include "readfile.h"
#include <iostream>

griddivide::griddivide(double* M, const int32_t M_num, const int32_t dim)
	: min_x(DBL_MAX), max_x(-min_x), min_y(DBL_MAX),
	  max_y(-min_y), min_z(DBL_MAX), max_z(-min_z),
	  num(M_num), dim(dim)
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
		if (isnan(z)) continue;

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
	IcpPointToPlane icp(T, p.size(), dim, 3);
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

double* RotateImage(double* M, int num0, int dim, int mode) {		// 旋转图像
	/*double* T = new double[num0 * 3];
	int index = 0;
	for (int i = 0; i < num0; ++i) {
		if (isnan(M[i * dim + 2]))
			continue;
		T[index * dim + 0] = M[i * dim + 0];
		T[index * dim + 1] = M[i * dim + 1];
		T[index * dim + 2] = M[i * dim + 2];
		index++;
	}*/
	// 获取法向量
	IcpPointToPlane icp(M, num0, dim);
	double *M_normal = icp.getM_normal();

	// 获取平均点
	double x0 = 0, y0 = 0, z0 = 0;
	for (int i = 0; i < num0; ++i) {
		x0 += M[i * dim + 0];
		y0 += M[i * dim + 1];
		z0 += M[i * dim + 2];
	}
	x0 /= num0;
	y0 /= num0;
	z0 /= num0;

	// 求所有点到平均点的距离及该点的权重和总法向量
	vector<double> dist(num0, 0), w(num0, 0);
	double max_dist = 0;
	vector<double> N(3, 0);
	for (int i = 0; i < num0; ++i) {
		double temp = sqrt(pow((M[i * dim + 0] - x0), 2) +
			pow((M[i * dim + 1] - y0), 2) + pow((M[i * dim + 2] - z0), 2));
		dist[i] = temp;
		if (temp > max_dist)
			max_dist = temp;
	}
	for (int i = 0; i < num0; ++i) {
		w[i] = (1 - dist[i] / max_dist) + 0.2; // 人为定义的权重
		/*N[0] += M_normal[i * dim + 0] * w[i] / num0;
		N[1] += M_normal[i * dim + 1] * w[i] / num0;
		N[2] += M_normal[i * dim + 2] * w[i] / num0;*/
		N[0] += M_normal[i * dim + 0] / num0;
		N[1] += M_normal[i * dim + 1] / num0;
		N[2] += M_normal[i * dim + 2] / num0;
	}
	//N[0] -= x0;
	//N[1] -= y0;
	//N[2] -= z0;
	// 求旋转角
	double Normal_N = norm_p(N);
	double thetax = asin(N[0] / Normal_N);	// xoz平面旋转角
	double thetay = asin(N[1] / Normal_N);	// yoz平面旋转角

	// 将坐标进行旋转
	double* M_new = new double[num0 * 3];
	double x1, y1, z1;
	for (int i = 0; i < num0; ++i) {
		M_new[i * dim + 0] = M[i * dim + 0];
		M_new[i * dim + 1] = M[i * dim + 1];
		M_new[i * dim + 2] = M[i * dim + 2];
		x1 = x0 + (M_new[i * dim + 0] - x0) * cos(thetax) - (M_new[i * dim + 2] - z0) * sin(thetax);
		z1 = z0 + (M_new[i * dim + 2] - z0) * cos(thetax) + (M_new[i * dim + 0] - x0) * sin(thetax);
		if (mode == 1)
			M_new[i * dim + 0] = x1;
		M_new[i * dim + 2] = z1;
		y1 = y0 + (M_new[i * dim + 1] - y0) * cos(thetay) - (M_new[i * dim + 2] - z0) * sin(thetay);
		z1 = z0 + (M_new[i * dim + 2] - z0) * cos(thetay) + (M_new[i * dim + 1] - y0) * sin(thetay);
		if (mode == 1)
			M_new[i * dim + 1] = y1;
		M_new[i * dim + 2] = z1;
	}
	return M_new;
}

double* griddivide::gridconvert(double* M, int& num, double* M_c) {
	//double *M_out = new double[n_x * n_y * dim];

	int count_p = 0;
	for (int i = 0; i < n_x; ++i) {
		for (int j = 0; j < n_y; ++j) {
			double temp = 0;
			int count = 0;
			for (int k = 0; k < n_z; ++k) {
				for (int k0 = 0; k0 < point[i + j * n_x + k * n_x * n_y].size(); ++k0)
					temp += M[point[i + j * n_x + k * n_x * n_y][k0] * dim + 2];
				count += point[i + j * n_x + k * n_x * n_y].size();
			}
			M_c[(i * n_y + j) * dim + 0] = i + 1;
			M_c[(i * n_y + j) * dim + 1] = j + 1;
			if (count) {
				M_c[(i * n_y + j) * dim + 2] = temp / count;
				count_p++;
			}
			else
				M_c[(i * n_y + j) * dim + 2] = NAN;
		}
	}
	num = count_p;
	double *M_out = new double[count_p * dim];
	int index = 0;
	for (int i = 0; i < n_x; ++i) {
		for (int j = 0; j < n_y; ++j) {
			if (!isnan(M_c[(i * n_y + j) * dim + 2])) {
				M_out[index * dim + 0] = M_c[(i * n_y + j) * dim + 0];
				M_out[index * dim + 1] = M_c[(i * n_y + j) * dim + 1];
				M_out[index * dim + 2] = M_c[(i * n_y + j) * dim + 2];
				index++;
			}
		}
	}
	return M_out;
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
			for(int k=0; k<n_z; k++) {
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
					if (isnan(M[point[i + j*n_x + k*n_x*n_y][a] * dim + 2]))
						continue;
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

Matrix fit_plane(double* M, int dim, int num)
{
	// 直接暴力求解
	// 令Ax+By+Cz+D=0，Q=(Ax+By+Cz+D)^2，求min(S=sum(Q))
	// dS/dA = sum(Ax^2+Bxy+Cxz+Dx), dS/dB = sum(Axy+By^2+Cyz+Dy)
	// dS/dC = sum(Axz+Byz+Cz^2+Dz), dS/dD = sum(Ax+By+Cz+D)
	// 不能这么求，这样求出来解为0
	// 假定C!=0, 那么可以表示为z=ax+by+c
	// 类似于之前的曲面拟合
	// 令S = sum((ax+by+c-z)^2)
	Matrix A(3, 3), b(3, 1);
	// S对a求导
	A.val[0][0] = SumVector(M, 2, 0, 0, num, dim);
	A.val[0][1] = SumVector(M, 1, 1, 0, num, dim);
	A.val[0][2] = SumVector(M, 1, 0, 0, num, dim);
	b.val[0][0] = SumVector(M, 1, 0, 1, num, dim);
	// S对b求导
	A.val[1][0] = SumVector(M, 1, 1, 0, num, dim);
	A.val[1][1] = SumVector(M, 0, 2, 0, num, dim);
	A.val[1][2] = SumVector(M, 0, 1, 0, num, dim);
	b.val[1][0] = SumVector(M, 0, 1, 1, num, dim);;
	// S对c求导
	A.val[2][0] = SumVector(M, 1, 0, 0, num, dim);
	A.val[2][1] = SumVector(M, 0, 1, 0, num, dim);
	A.val[2][2] = SumVector(M, 0, 0, 0, num, dim);
	b.val[2][0] = SumVector(M, 0, 0, 1, num, dim);

	b.solve(A);
	return b;
}

// 2017/04/20修改网格划分和聚类方法
griddivide_new::griddivide_new(double* M, const int32_t M_num, const int32_t dim)
	: min_x(DBL_MAX), max_x(-min_x), min_y(DBL_MAX),
	  max_y(-min_y), min_z(DBL_MAX), max_z(-min_z),
	  num(M_num), dim(dim) {
	for (int i = 0; i<M_num; i++) {
		if (min_x > M[i*dim + 0])
			min_x = M[i*dim + 0];
		if (max_x < M[i*dim + 0])
			max_x = M[i*dim + 0];
		if (min_y > M[i*dim + 1])
			min_y = M[i*dim + 1];
		if (max_y < M[i*dim + 1])
			max_y = M[i*dim + 1];
		if (min_z > M[i*dim + 2])
			min_z = M[i*dim + 2];
		if (max_z < M[i*dim + 2])
			max_z = M[i*dim + 2];
	}
}

void griddivide_new::gridpoint(double* M, double cubsize) {
	// cubsize为网格的边长
	n_x = (int)((max_x - min_x) / cubsize + 0.5);
	n_y = (int)((max_y - min_y) / cubsize + 0.5);
	n_z = (int)((max_z - min_z) / cubsize + 0.5);
	point.resize(n_x*n_y*n_z);

	for (int i = 0; i < num; i++) {
		double x = M[i*dim + 0];
		double y = M[i*dim + 1];
		double z = M[i*dim + 2];
		if (z == NAN) continue;

		// 三维空间长a、宽b、高c的坐标表示为a+b*nx+c*nx*ny
		int grid_x = ((int)((x - min_x) / cubsize));
		int grid_y = ((int)((y - min_y) / cubsize));
		int grid_z = ((int)((z - min_z) / cubsize));
		point[grid_x + grid_y * n_x + grid_z * n_x * n_y].push_back(i);
	}
}

double* griddivide_new::grid_filter(double* M, int& count, int min_p, int mode) {
	// mode表示滤波模式，1是表示均值，2是直接去噪
	vector<vector<double>> m_p;
	//if (dim != 3)
	//	return m_p; 

	count = 0; // 计数，记录有用点的个数
	for (int i = 0; i < n_x * n_y * n_z; ++i) {
		if (point[i].size() < min_p)
			continue;
		
		if (mode == 1) {
			count++;
			vector<double> tmp_p;
			double temp_x = 0, temp_y = 0, temp_z = 0;
			for (int j = 0; j < point[i].size(); ++j) {
				temp_x += M[point[i][j] * dim + 0];
				temp_y += M[point[i][j] * dim + 1];
				temp_z += M[point[i][j] * dim + 2];
			}
			temp_x /= point[i].size();
			temp_y /= point[i].size();
			temp_z /= point[i].size();
			tmp_p.push_back(temp_x);
			tmp_p.push_back(temp_y);
			tmp_p.push_back(temp_z);
			m_p.push_back(tmp_p);
		}
		else if (mode == 2) {
			count += point[i].size();
		}
	}
	double* M_new = new double[count * dim];
	if (mode == 1) {
		for (int i = 0; i < count; ++i) {
			M_new[i * dim + 0] = m_p[i][0];
			M_new[i * dim + 1] = m_p[i][1];
			M_new[i * dim + 2] = m_p[i][2];
		}
	}
	else if (mode == 2) {
		int k = 0;
		for (int i = 0; i < n_x * n_y * n_z; ++i) {
			if (point[i].size() < min_p)
				continue;
			for (int j = 0; j < point[i].size(); j++) {
				M_new[k * dim + 0] = M[point[i][j] * dim + 0];
				M_new[k * dim + 1] = M[point[i][j] * dim + 1];
				M_new[k * dim + 2] = M[point[i][j] * dim + 2];
				k++;
			}
		}
	}
	return M_new;
	
}

// 获取方差
double GetVariance(vector<int> num, double aver) {
	double var = 0;
	for (int i = 0; i < num.size(); ++i) {
		var += pow(num[i] - aver, 2);
	}
	var /= (num.size() - 1);
	return var;
}
// 获取点到Kmeans中点的距离最近的index
int GetIndexOfKmeans(vector<vector<double>> Kmeans, double* M, int index, int dim) {
	int res = 0;
	double temp = 0;
	for (int i = 0; i < Kmeans.size(); ++i) {
		double x = M[index * dim + 0];
		double y = M[index * dim + 1];
		double z = M[index * dim + 2];
		if (i == 0) {
			// z方向的距离要近的多，只用z方向来做聚类
			temp = abs(Kmeans[i][2] - z);
			res = i;
		} else {
			if (abs(Kmeans[i][2] - z) < temp) {
				temp = abs(Kmeans[i][2] - z);
				res = i;
			}
		}
	}
	return res;
}

// 用kmeans聚类方法，一共k个类
vector<vector<double>> griddivide_new::grid_kmeans(double* M, int k, int num) {
	// 迭代100次，取z向相差最大的为聚类中心
	vector<vector<double>> Kmeans(k, vector<double>(3, -1));
	double temp;
	for (int i = 0; i < 100; ++i) {
		vector<int> kcluster(k);
		double aver = 0;
		for (int j = 0; j < k; ++j) {
			kcluster[j] = rand() % num;
			aver += M[kcluster[j] * dim + 2];
		}
		aver /= k;
		if (i > 0) {
			if (GetVariance(kcluster, aver) > temp) {
				temp = GetVariance(kcluster, aver);
				for (int j = 0; j < k; ++j) {
					Kmeans[j][0] = M[kcluster[j] * dim + 0];
					Kmeans[j][1] = M[kcluster[j] * dim + 1];
					Kmeans[j][2] = M[kcluster[j] * dim + 2];
				}
			}
		}
		else {
			for (int j = 0; j < k; ++j) {
				temp = GetVariance(kcluster, aver);
				Kmeans[j][0] = M[kcluster[j] * dim + 0];
				Kmeans[j][1] = M[kcluster[j] * dim + 1];
				Kmeans[j][2] = M[kcluster[j] * dim + 2];
			}
		}
	}

	// 开始聚类，对离第K类最近的点
	vector<vector<double>> cluster(k);
	vector<vector<double>> SumOfCluster(k, vector<double>(2, 0));
	for (int i = 0; i < num; ++i) {
		int index = GetIndexOfKmeans(Kmeans, M, i, dim);
		SumOfCluster[index][0] += M[i * dim + 2];
		SumOfCluster[index][1] += 1;
		cluster[index].push_back(M[i * dim + 0]);
		cluster[index].push_back(M[i * dim + 1]);
		cluster[index].push_back(M[i * dim + 2]);
		Kmeans[index][2] = SumOfCluster[index][0] / SumOfCluster[index][1];
	}
	return cluster;
}