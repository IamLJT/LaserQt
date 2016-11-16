#include <iostream>
#include "icpPointToPoint.h"
#include "icpPointToPlane.h"
#include "readfile.h"
#include "Filter.h"
#include "PointCloudAlgorithm.h"

using namespace std;

void PointCloudDenoise(const char* path) {
	int32_t dim = 3, num = 0;
	vector<int> DataFile(4, 0);
	double *M = ReadFile(path, DataFile);

	num = DataFile[0];
	dim = DataFile[1];
	char OutPath[] = "/home/summychou/Github/LaserQt/code/LaserQt_Material/tempData.txt";

	Filter flr(M, num, dim);

	double *M0 = flr.SimpleFilter();
	WriteFile(OutPath, M0, num, dim);
}

void PointCloudFitting(const char* path, bool isFilter, const char* targetData) {
	int32_t dim = 3, num = 0, m = 0, n = 0;
	vector<int> DataFile(4, 0);
	double *M;
	double *T = ReadFile(targetData, DataFile);
	if(false == isFilter)
		M = ReadFile(targetData, DataFile);
	else
		M = ReadFile(path, DataFile);

	num = DataFile[0];
	dim = DataFile[1];
	m = DataFile[2];
	n = DataFile[3];

	Matrix R = Matrix::eye(3);
	Matrix t(3,1);

	cout << endl << "Running ICP (point-to-plane, no outliers)" << endl;
	IcpPointToPlane icp(M, num, dim);
	icp.fit(T, num, R, t, -1);

	Matrix mx = Matrix::ArrayToMatrix(M, m, n, dim);
	Matrix res = R*(~mx) + t;

	double *M0 = Matrix::MatrixToArray(res, dim);

	char OutPath[] = "/home/summychou/Github/LaserQt/code/LaserQt_Material/输出数据.txt";
	WriteFile(OutPath, M0, num, dim);
}
