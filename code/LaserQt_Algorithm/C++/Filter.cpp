#include "Filter.h"
#include <algorithm>
#include <vector>

using namespace std;

double Filter::GetMedian(Matrix mx, int row, int col)
{
	//	core is 3*3
	vector<double> val;
	for(int i=row-1; i<=row+1; i++)
	{
		for(int j=col-1; j<=col+1; j++)
		{
			if(i<0||i>=mx.m||j<0||j>=mx.n)
				continue;
			val.push_back(mx.val[i][j]);
		}
	}
	sort(val.begin(), val.end());
	//	get the median number
	if(val.size()%2)
		return val[val.size()/2];
	else
		return (val[val.size()/2-1]+val[val.size()/2])/2;
}

double* Filter::SimpleFilter()
{
	/*
	//	Mesh Denoise
	vector<double> x,y,z;
	double x_min=DBL_MAX, x_max=DBL_MIN, y_min=DBL_MAX, y_max=DBL_MIN, z_min=DBL_MAX, z_max=DBL_MIN;
	if(3==dim)
	{
		for(int i=0; i<M_num*dim; i+=dim)
		{
			x.push_back(M[i]);
			x_min=x_min>M[i]?M[i]:x_min;
			x_max=x_max<M[i]?M[i]:x_max;
			y.push_back(M[i+1]);
			y_min=y_min>M[i]?M[i]:y_min;
			y_max=y_max<M[i]?M[i]:y_max;
			z.push_back(M[i+2]);
			z_min=z_min>M[i]?M[i]:z_min;
			z_max=z_max<M[i]?M[i]:z_max;
		}
		int cell_size_x=5, cell_size_y=5;
		int M=(int)((x_max+1)-(x_min-1))/cell_size_x+1;
		int N=(int)((y_max+1)-(y_min-1))/cell_size_y+1;
		int L=100;
		int cell_size_z=(int)((z_max+1)-(z_min+1))/L-1;
	}
	*/
	//	Median Filter
	//	The Data is (row, col, value)
	Matrix mx(100, 100);		//	dst-data is 100*100
	int row, col;
	for(int i=0; i<M_num*dim; i+=dim)
	{
		row=M[i]-1;
		col=M[i+1]-1;
		mx.val[row][col]=M[i+2];
	}
	//Matrix res(mx);
	double *r = new double[M_num*dim];	//	Do not change the src-data
	for(int i=0; i<mx.m; i++){
		for(int j=0; j<mx.n; j++){
			r[dim*(i*mx.n+j)]=i+1;
			r[dim*(i*mx.n+j)+1]=i+1;
			r[dim*(i*mx.n+j)+2]=GetMedian(mx,i,j);
		}
	}
	return r;
}