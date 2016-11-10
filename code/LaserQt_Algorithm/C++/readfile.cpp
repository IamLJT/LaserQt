#include "readfile.h"

/*
 * 函数名：ReadFile
 * 功能简介： 读取点云数据
 * 输入参数： path - ; numOfPoints - 
 * 输出参数： M - 
*/
double* ReadFile(char* path, int32_t& numOfPoints) {
	FILE* fp;
	fp = fopen(path, "r");
	std::vector<double> dataVector;

	while (!feof(fp)) {
		double input_data01, input_data02, input_data03;
		fscanf(fp, "%lf, %lf, %lf", &input_data01, &input_data02, &input_data03);
		dataVector.push_back(idata1);
		dataVector.push_back(idata2);
		dataVector.push_back(idata3);
	}
	fclose(fp);

	int size = (int)dataVector.size();
	double* dataMatrix = new double[size];
	for (int i = 0; i < size; i++) {
		dataMatrix[i] = dataVector[i];
	}
		
	numOfPoints = size / 3;
	
	return dataMatrix;
}
