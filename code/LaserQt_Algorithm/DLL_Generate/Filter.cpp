#include "Filter.h"
#include <algorithm>
#include <vector>
#include <cmath>

using namespace std;

//	Initial Filter
Filter::Filter(double *M, const int32_t M_num, const int32_t dim, int m, int n)
	:M(M),M_num(M_num),dim(dim),m(m),n(n)
{
	noisenum = 0;
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

void Filter::copyData(double* M, int dim, int m, int n)
{
	mx = Matrix::ArrayToMatrix(M, m, n, dim);
}

double Filter::GetChordHeight(Matrix mx, bool direc, int row, int col)
	//	获取弦高
{
	int x1, x2, y1, y2;
	double z1, z2;
	if(direc == 0)
	{
		if(row == 0)
			x1 = row, x2 = row + 1;
		else if(row == mx.m - 1)
			x1 = row -1, x2 = row;
		else
			x1 = row - 1, x2 = row + 1;
		y1 = col, y2 = col;
		z1 = mx.val[x1][y1];
		z2 = mx.val[x2][y2];
	}
	else
	{
		if(col == 0)
			y1 = col, y2 = col + 1;
		else if(col == mx.n - 1)
			y1 = col - 1, y2 = col;
		else
			y1 = col - 1, y2 = col + 1;
		x1 = row, x2 = row;
		z1 = mx.val[x1][y1];
		z2 = mx.val[x2][y2];
	}
	double a = sqrt((row - x1) * (row - x1) + (col - y1) * (col - y1) + (mx.val[row][col] - z1) * (mx.val[row][col] - z1));
	double b = sqrt((row - x2) * (row - x2) + (col - y2) * (col - y2) + (mx.val[row][col] - z2) * (mx.val[row][col] - z2));
	double c = sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1) + (z2 - z1) * (z2 - z1));
	double p = (a + b + c)/2;
	if(c == 0)
	{
		cout << "Wrong data in get chord height!" << endl;
		return 0;
	}
	else
		return 2 * sqrt(p * (p - a) * (p - b) * (p - c)) / c;	//	海伦公式求弦高
}

double* Filter::ThresholdFilter(double threshold)	//	阈值法求解噪声点数
{
	Matrix r(mx);
	for(int i=0; i<mx.m; i++)
	{
		for(int j=0; j<mx.n; j++)
		{
			if(GetChordHeight(r, 0, i, j) > threshold)
			//if(i >= 1 && i <mx.m-1 && r.val[i][j] - (mx.val[i-1][j] + mx.val[i+1][j])/2 > threshold)
				r.val[i][j] = (r.val[i-1][j] + r.val[i+1][j])/2;
			else if(GetChordHeight(r, 1, i, j) > threshold)
			//else if(j >= 1 && j <mx.n-1 && r.val[i][j] - (mx.val[i][j-1] + mx.val[i][j+1])/2 > threshold)
				r.val[i][j] = (r.val[i][j-1] + r.val[i][j+1])/2;
			else
				continue;
			noisenum ++;
		}
	}
	double *res = Matrix::MatrixToArray(r, dim);
	return res;
}

double Filter::GetMedian(Matrix mx, int w_core, int row, int col)
	//	 获取算子的中值
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
	//	获取算子的均值
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
	double *r = new double[M_num*dim];	//	Do not change the source-data
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

//	Get the value after Gaussian Filter和α Mean Filter
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

//	双边滤波：距离和强度同时加入判决条件
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

double* Filter::FurtherFilter()	//	未实现
{
	return 0;
}