#include "readfile.h"

extern "C" __declspec(dllexport) double* ReadFile(char* strPath, int32_t& num, int32_t& dim)	
	// Read file data one by one
{
	/*
	std::ifstream fin(strPath);
	std::vector<double> vec;
	while(fin)
	{
		double idata;
		fin >> idata;
		vec.push_back(idata);	//	can't read?
	}	*/
	FILE *fp;
	fp = fopen(strPath, "r");
	std::vector<double> vec;
	num = 0;
	while(!feof(fp))
	{
		double idata1, idata2, idata3;
		fscanf(fp, "%lf,%lf,%lf", &idata1,&idata2,&idata3);
		dim=3;
		vec.push_back(idata1);
		vec.push_back(idata2);
		vec.push_back(idata3);
		num++;
	}
	double *M = new double[(int)vec.size()];
	for(int i=0; i<(int)vec.size(); i++)
		M[i]=vec[i];
	//num=(int)vec.size()/3;		//	icp need it!
	fclose(fp);
	return M;
}

extern "C" __declspec(dllexport) void WriteFile(char* strPath, double* M, int32_t num, int32_t dim)
{
	FILE *fp;
	fp = fopen(strPath, "w");
	for(int i=0; i<num*dim; i+=dim)
	{
		fprintf(fp, "%lf,%lf,%lf\n", M[i], M[i+1], M[i+2]);
	}
	fclose(fp);
}