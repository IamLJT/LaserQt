#include <direct.h>
#include <iostream>
#include <windows.h>
#include "Filter.h"
#include "icpPointToPoint.h"
#include "icpPointToPlane.h"
#include "readfile.h"
#include "GridDivide.h"

using namespace std;

#ifndef _MAX_
	#define MAX 256
#endif _MAX_

BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved) {
    switch (ul_reason_for_call) {
		case DLL_PROCESS_ATTACH:
			printf("DLL_PROCESS_ATTACH\n");
			break;
		case DLL_THREAD_ATTACH:
			printf("DLL_THREAD_ATTACH\n");
			break;
		case DLL_THREAD_DETACH:
			printf("DLL_THREAD_DETACH\n");
			break;
		case DLL_PROCESS_DETACH:
			printf("DLL_PROCESS_DETACH\n");
			break;
	}
    return TRUE;
}

extern "C" _declspec(dllexport) int PointCloudKThreshlod(const char* Path) {
	int32_t dim = 3, num = 0, m = 0, n = 0;
	vector<int> DataFile(4, 0);
	double *M = ReadFile(Path, DataFile);

	num = DataFile[0];
	dim = DataFile[1];
	m = DataFile[2];
	n = DataFile[3];

	/*Filter flr(M, num, dim, m, n);

	double *M0 = flr.ThresholdFilter(20);*/

	int num_G = 0;
	griddivide Grid_temp(M, num, dim);
	Grid_temp.dividenum(30, 30, 10);
	Grid_temp.grid_point(M, num, dim);
	double* M0 = Grid_temp.first_filter_grid(M, num_G, dim);

	char sPath[MAX];
	getcwd(sPath, MAX_PATH);
	strcat(sPath, "\\LaserQt_Material\\TempData.txt");
	WriteFile(sPath, M0, num, dim);

	return num-num_G;
}

extern "C" _declspec(dllexport) void PointCloudDenoise() {
	char Path[MAX];
	getcwd(Path, MAX_PATH);
	strcat(Path, "\\LaserQt_Material\\TempData.txt");

	int32_t dim = 3, num = 0, m = 0, n = 0;
	vector<int> DataFile(4, 0);
	double *M = ReadFile(Path, DataFile);

	num = DataFile[0];
	dim = DataFile[1];
	m = DataFile[2];
	n = DataFile[3];

	Filter flr(M, num, dim, m, n);
	double *M0 = flr.SimpleFilter();

	flr.copyData(M0, dim, m, n);
	M0 = flr.bFilter2();

	WriteFile(Path, M0, num, dim);
}

extern "C" _declspec(dllexport) void PointCloudFitting(const char *inPath, bool isFilter, const char *TargetData) {
	char Path[MAX];
	getcwd(Path, MAX_PATH);
	strcat(Path, "\\LaserQt_Material\\TempData.txt");

	int32_t dim = 3, num = 0, m = 0, n = 0;
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
	IcpPointToPlane icp(T, num, dim);
	icp.fit(M,num,R,t,-1);
	//	T is dest-matrix, num is number of data
	//	R and t means Ratate and Translate Matrix

	Matrix mx = Matrix::ArrayToMatrix(M, m, n, dim);

	double *M0 = new double[mx.m * mx.n];
	double r00 = R.val[0][0]; double r01 = R.val[0][1]; double r02 = R.val[0][2];
	double r10 = R.val[1][0]; double r11 = R.val[1][1]; double r12 = R.val[1][2];
	double r20 = R.val[2][0]; double r21 = R.val[2][1]; double r22 = R.val[2][2];
	double t0  = t.val[0][0]; double t1  = t.val[1][0]; double t2  = t.val[2][0];

	for(int idx=0; idx<mx.m; idx++)
	{
		M0[idx*3+0] = r00*mx.val[idx][0] + r01*mx.val[idx][1] + r02*mx.val[idx][2] + t0;
		M0[idx*3+1] = r10*mx.val[idx][0] + r11*mx.val[idx][1] + r12*mx.val[idx][2] + t1;
		M0[idx*3+2] = r20*mx.val[idx][0] + r21*mx.val[idx][1] + r22*mx.val[idx][2] + t2;
	}

	char OutPath[MAX];
	getcwd(OutPath, MAX_PATH);
	strcat(OutPath, "\\LaserQt_Material\\FittingData.txt");

	WriteFile(OutPath, M0, num, dim);
}