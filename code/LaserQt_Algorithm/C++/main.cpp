#include <iostream>
#include "icpPointToPoint.h"
#include "icpPointToPlane.h"
#include "readfile.h"
#include "Filter.h"

using namespace std;

int main (int argc, char** argv) {

	//int32_t dim = 3, num=0;	//	dim means dimension��only can be 2 or 3; num is number of data.

	int32_t dim = 3, num=0, m = 0, n = 0;
	vector<int> DataFile(4, 0);

	char str1[]="../../LaserQt_Material/测试数据.txt";
	char str2[]="../../LaserQt_Material/目标数据.txt";
	//	name of Path

	double *M = ReadFile(str1, DataFile);		// ��ʼֵ

	num = DataFile[0];
	dim = DataFile[1];
	//char OutPath[] = "..\��������.txt";
	char path1[]="../../LaserQt_Material/输出数据.txt";

	Filter flr(M, num, dim);		//	Filter

	double *M0=flr.SimpleFilter();
	WriteFile(path1, M0, num, dim);

	bool isFilter = true;
	double *T = ReadFile(str2, DataFile);
	double *M1;
	if(false == isFilter)
		M1 = ReadFile(str1, DataFile);
	else
		M1 = ReadFile(path1, DataFile);

	num = DataFile[0];
	dim = DataFile[1];
	m = DataFile[2];
	n = DataFile[3];

	// start with identity as initial transformation
	// in practice you might want to use some kind of prediction here
	Matrix R = Matrix::eye(3);
	Matrix t(3,1);

	// run point-to-plane ICP (-1 = no outlier threshold)
	cout << endl << "Running ICP (point-to-plane, no outliers)" << endl;
	IcpPointToPlane icp(M1, num, dim);
	icp.fit(T,num,R,t,-1);
	//	T is dest-matrix, num is number of data
	//	R and t means Ratate and Translate Matrix

	Matrix mx = Matrix::ArrayToMatrix(M1, m, n, dim);
	Matrix res = R*(~mx) ;
	res = ~res;

	for(int i = 0; i<res.m; i++)
	{
		res.val[i][0] += t.val[0][0];
		res.val[i][1] += t.val[1][0];
		res.val[i][2] += t.val[2][0];
	}

	double *M2 = Matrix::MatrixToArray(res, dim);

	//char OutPath[] = "..\��������.txt";
	char path2[]="../../LaserQt_Material/输出数据.txt";
	WriteFile(path2, M2, num, dim);

	return 0;
}