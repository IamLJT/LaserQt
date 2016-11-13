#include <iostream>
#include "icpPointToPoint.h"
#include "icpPointToPlane.h"
#include "readfile.h"
#include "Filter.h"
#include "PointCloudAlgorithm.h"

using namespace std;

void PointCloudDenoise()
{
	int32_t dim = 3, num=0;	//	dim means dimension��only can be 2 or 3; num is number of data.
	vector<int> DataFile(4, 0);
	double *M = ReadFile("/home/summychou/Github/LaserQt/code/LaserQt_Material/测试数据.txt", DataFile);

	num = DataFile[0];
	dim = DataFile[1];
	char OutPath[] = "/home/summychou/Github/LaserQt/code/LaserQt_Material/tempData.txt";

	Filter flr(M, num, dim);		//	Filter

	double *M0=flr.SimpleFilter();
	WriteFile(OutPath, M0, num, dim);
}

void PointCloudFitting(const char* Path, const char *inPath, bool isFilter, const char *TargetData)
{
	int32_t dim = 3, num=0, m = 0, n = 0;
	vector<int> DataFile(4, 0);
	double *M;
	double *T = ReadFile(TargetData, DataFile);
	if(false == isFilter)
		M = ReadFile(inPath, DataFile);
	else
		M = ReadFile(Path, DataFile);

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
	IcpPointToPlane icp(M, num, dim);
	icp.fit(T,num,R,t,-1);
	//	T is dest-matrix, num is number of data
	//	R and t means Ratate and Translate Matrix

	Matrix mx = Matrix::ArrayToMatrix(M, m, n, dim);
	Matrix res = R*(~mx) + t;

	double *M0 = Matrix::MatrixToArray(res, dim);

	char OutPath[] = "..\��������.txt";
	WriteFile(OutPath, M0, num, dim);
}