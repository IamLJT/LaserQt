#include "readfile.h"

double* ReadFile(char* strPath, int32_t& num)	
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
	while(!feof(fp))
	{
		double idata1, idata2, idata3;
		fscanf(fp, "%lf,%lf,%lf", &idata1,&idata2,&idata3);
		vec.push_back(idata1);
		vec.push_back(idata2);
		vec.push_back(idata3);
	}
	double *M = new double[(int)vec.size()];
	for(int i=0; i<(int)vec.size(); i++)
		M[i]=vec[i];
	num=(int)vec.size()/3;		//	icp need it!
	fclose(fp);
	return M;
}