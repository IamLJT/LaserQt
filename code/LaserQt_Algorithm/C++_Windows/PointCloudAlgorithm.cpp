#include <iostream>
#include "icpPointToPoint.h"
#include "icpPointToPlane.h"
#include "readfile.h"
#include "Filter.h"
#include <windows.h>
#include  <direct.h>

#ifndef _MAX_
#define MAX 256
#endif _MAX_

using namespace std;

BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved)
{  
    switch (ul_reason_for_call)  
    {  
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

extern "C" _declspec(dllexport) int PointCloudKThreshlod(const char* Path)
{
	int32_t dim = 3, num=0, m = 0, n=0;	//	dim means dimension��only can be 2 or 3; num is number of data.
	vector<int> DataFile(4, 0);
	double *M = ReadFile(Path, DataFile);

	num = DataFile[0];
	dim = DataFile[1];
	m = DataFile[2];
	n = DataFile[3];

	Filter flr(M, num, dim, m, n);		//	Filter

	double *M0 = flr.ThresholdFilter(20);

	char sPath[MAX];
	getcwd(sPath, MAX_PATH);

	strcat(sPath, "\\LaserQt_Material\\TempData.txt");
	WriteFile(sPath, M0, num, dim);

	return flr.noisenum;
}

extern "C" _declspec(dllexport) void PointCloudDenoise()
{
	char Path[MAX];
	getcwd(Path, MAX_PATH);
	strcat(Path, "\\LaserQt_Material\\TempData.txt");

	int32_t dim = 3, num=0, m = 0, n=0;	//	dim means dimension��only can be 2 or 3; num is number of data.
	vector<int> DataFile(4, 0);

	// ����
	//char Path[] = "D:/�о���/��Ŀ/����ɨ������������/LaserQt/code/LaserQt_Material/��������.txt";
	double *M = ReadFile(Path, DataFile);

	num = DataFile[0];
	dim = DataFile[1];
	m = DataFile[2];
	n = DataFile[3];

	Filter flr(M, num, dim, m, n);		//	Filter
	double *M0 = flr.SimpleFilter();

	flr.copyData(M0, dim, m, n);
	M0 = flr.bFilter2();

	WriteFile(Path, M0, num, dim);
}

extern "C" _declspec(dllexport) void PointCloudFitting(const char *inPath, bool isFilter, const char *TargetData)
	//	inPathΪ��ʼ·���� isFilter��ʾ�Ƿ��ѱ�ȥ�룬TargetDataΪĿ������·��
{
	char Path[MAX];
	getcwd(Path, MAX_PATH);
	strcat(Path, "\\LaserQt_Material\\TempData.txt");
	//	PathΪ�м�ֵ

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
	IcpPointToPlane icp(T, num, dim);
	icp.fit(M,num,R,t,-1);
	//	T is dest-matrix, num is number of data
	//	R and t means Ratate and Translate Matrix

	Matrix mx = Matrix::ArrayToMatrix(M, m, n, dim);
	//Matrix res = R*(~mx);
	/*for(int i=0; i<res.n; i++)
	{
		res.val[0][i] += t.val[0][0];
		res.val[1][i] += t.val[1][0];
		res.val[2][i] += t.val[2][0];
	}*/

	//	������Ϻ�ľ���
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

	//double *M0 = Matrix::MatrixToArray(res, dim);

	char OutPath[MAX];
	getcwd(OutPath, MAX_PATH);
	strcat(OutPath, "\\LaserQt_Material\\�������.txt");

	WriteFile(OutPath, M0, num, dim);
}