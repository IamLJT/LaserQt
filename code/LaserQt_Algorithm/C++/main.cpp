#include <iostream>
#include "icpPointToPoint.h"
#include "icpPointToPlane.h"
#include "readfile.h"

using namespace std;

int main (int argc, char** argv) {

	int32_t dim = 3, num = 0;  // dim means dimension��only can be 2 or 3; num is number of data.

	char* pathForTestingDataFile = "./LaserQt_Material/测试数据.txt";  // 数据文件路径名
	char* pathForTargetDataFile = "./LaserQt_Material/目标数据.txt";  // 数据文件路径名

	double* M = ReadFile(pathForTestingDataFile, num);
	double* T = ReadFile(pathForTargetDataFile, num);

	// start with identity as initial transformation
	// in practice you might want to use some kind of prediction here
	Matrix R = Matrix::eye(3);
	Matrix t(3, 1);

	// run point-to-plane ICP (-1 = no outlier threshold)
	cout << endl << "Running ICP (point-to-plane, no outliers)" << endl;
	IcpPointToPlane icp(M,num,dim);
	icp.fit(T, num, R, t, -1);
	//	T is dest-matrix, num is number of data
	//	R and t means Ratate and Translate Matrix

	// results
	cout << endl << "Transformation results:" << endl;
	cout << "R:" << endl << R << endl << endl;
	cout << "t:" << endl << t << endl << endl;

	// free memory
	free(M);
	free(T);
 
	return 0;
}
