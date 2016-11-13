#include "readfile.h"
#include <vector>

double* ReadFile(const char* strPath, std::vector<int>& DataFile)	
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
	int num = 0, dim = 3;
	double idata1, idata2, idata3;
	while(!feof(fp))
	{
		fscanf(fp, "%lf,%lf,%lf", &idata1,&idata2,&idata3);
		vec.push_back(idata1);
		vec.push_back(idata2);
		vec.push_back(idata3);
		num++;
	}
	DataFile[0] = num;
	DataFile[1] = dim;
	DataFile[2] = idata1;
	DataFile[3] = idata2;
	double *M = new double[(int)vec.size()];
	for(int i=0; i<(int)vec.size(); i++)
		M[i]=vec[i];
	//num=(int)vec.size()/3;		//	icp need it!
	fclose(fp);
	return M;
}

void WriteFile(char* strPath, double* M, int32_t num, int32_t dim)
{
	FILE *fp;
	fp = fopen(strPath, "w");
	for(int i=0; i<num*dim; i+=dim)
	{
		if(i<(num-1)*dim)
			fprintf(fp, "%lf,%lf,%lf\n", M[i], M[i+1], M[i+2]);
		else
			fprintf(fp, "%lf,%lf,%lf", M[i], M[i+1], M[i+2]);
	}
	fclose(fp);
}