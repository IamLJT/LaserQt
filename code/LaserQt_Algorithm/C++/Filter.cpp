#include "Filter.h"
#include <algorithm>
#include <vector>
#include <cmath>

using namespace std;

//	Initial Filter
Filter::Filter(double *M, const int32_t M_num, const int32_t dim, int m, int n)
	:M(M),M_num(M_num),dim(dim),m(m),n(n)
{
	Matrix r(m,n);
	mx = r;
	int row, col;
	for(int i=0; i<M_num*dim; i+=dim)
	{
		row=M[i]-1;
		col=M[i+1]-1;
		mx.val[row][col]=M[i+2];
	}
}

double Filter::GetMedian(Matrix mx, int w_core, int row, int col)
{
	//	core is 3*3
	vector<double> val;
	for(int i=row-w_core; i<=row+w_core; i++)
	{
		for(int j=col-w_core; j<=col+w_core; j++)
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

double Filter::GetMean(Matrix mx, int w_core, int row, int col)
{
	double sum=0;
	int num=0;
	for(int i=row-w_core; i<=row+w_core; i++)
	{
		for(int j=col-w_core; j<=col+w_core; j++)
		{
			if(i<0||i>=mx.m||j<0||j>=mx.n)
				continue;
			sum += mx.val[i][j];
			num ++;
		}
	}
	if(num!=0)
		return sum/num;
	else
	{
		cout << "Wrong matrix in calculating Mean number!\n";
		return 0;
	}
}

double* Filter::SimpleFilter()
{
	//	Median Filter
	//	The Data is (row, col, value)
	
	//Matrix res(mx);
	int w_core = 1;
	double *r = new double[M_num*dim];	//	Do not change the src-data
	for(int i=0; i<mx.m; i++){
		for(int j=0; j<mx.n; j++){
			r[dim*(i*mx.n+j)]=i+1;
			r[dim*(i*mx.n+j)+1]=j+1;
			r[dim*(i*mx.n+j)+2]=GetMedian(mx,w_core, i,j);
		}
	}
	for(int i=0; i<mx.m; i++){
		for(int j=0; j<mx.n; j++){
			r[dim*(i*mx.n+j)+2]=GetMean(mx,w_core,i,j);
		}
	}
	return r;
}

//	Get the value after Gaussian FilterºÍ¦Á Mean Filter
double Filter::GetBFilter2(Matrix mx, int w_core, int row, int col, int sigma_s, int sigma_r)
{
	double sum_img = 0, sum_wgt = 0;
	for(int i=row-w_core; i<=row+w_core; i++)
	{
		for(int j=col-w_core; j<=col+w_core; j++)
		{
			if(i<0 || i>=mx.m || j<0 || j>=mx.n)
				continue;
			sum_img += mx.val[i][j]*exp(-((row-i)*(row-i)+(col-j)*(col-j))/(2*sigma_s*sigma_s)
				-(mx.val[i][j]-mx.val[row][col])*(mx.val[i][j]-mx.val[row][col]))/(2*sigma_r*sigma_r);
			sum_wgt += exp(-((row-i)*(row-i)+(col-j)*(col-j))/(2*sigma_s*sigma_s)
				-(mx.val[i][j]-mx.val[row][col])*(mx.val[i][j]-mx.val[row][col]))/(2*sigma_r*sigma_r);
		}
	}
	if(sum_wgt==0) 
	{
		cout << "Wrong Matrix in calculating weight!\n";
		return 0;
	}
	else
		return sum_img/sum_wgt;
}

double* Filter::bFilter2()
{
	Matrix r(mx);
	int w_core = 2;
	for(int i=0; i<mx.m; i++)
	{
		for(int j=0; j<mx.n; j++)
		{
			r.val[i][j] = GetBFilter2(mx, w_core, i, j, 10, 30);
		}
	}
	double *res = Matrix::MatrixToArray(r, dim);
	return res;
}

