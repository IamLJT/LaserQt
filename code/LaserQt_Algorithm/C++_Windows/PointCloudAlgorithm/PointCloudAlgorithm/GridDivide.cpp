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

	for(int i=0; i<M_num; i++)
	{
		double x = M[i*dim + 0];
		double y = M[i*dim + 1];
		double z = M[i*dim + 2];

		// 三维空间长a、宽b、高c的坐标表示为a+b*nx+c*nx*ny

		point[((int)((x-min_x)/interval_x)) + ((int)((y-min_y)/interval_y)) * n_x + 
			((int)((z-min_z)/interval_z)) * n_x * n_y].push_back(i);
	}
}

double* griddivide::first_filter_grid(double* M, int& num_G, int dim)
{
	for(int i=0; i<(int)point.size(); i++)
	{
		if(point[i].size() && point[i].size() < 5)
			point[i].clear();	//	去除第一类噪声点
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
				if(temp_p[i+j*n_x+k*n_x*n_y]!=kk+1)
					point[i+j*n_x+k*n_x*n_y].clear();
			}
		}
	}
	
	//	还需要其他的滤波措施，所以与清除第二类噪声点分开
	for(int i=0; i<n_x; i++){
		for(int j=0; j<n_y; j++){
			for(int k=0; k<n_z; k++)
			{
				for(int a=0; a<point[i+j*n_x+k*n_x*n_y].size(); a++)
				{
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