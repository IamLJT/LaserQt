#ifndef ICP_POINT_TO_PLANE_H
#define ICP_POINT_TO_PLANE_H

#include "icp.h"
using namespace std;

class IcpPointToPlane : public Icp {

public:
  
	IcpPointToPlane (double *M,const int32_t M_num,const int32_t dim,const int32_t num_neighbors=10,const double flatness=5.0) : Icp(M,M_num,dim) {
	M_normal = computeNormals(num_neighbors,flatness);
	}

	double* getM_normal() { return M_normal; }
	std::vector<int> getNearest(int index, double r, std::vector<bool>& isvisited);
	vector<vector<double>> getcluster(int min_p, double r, vector<bool>& isvisited);

	virtual ~IcpPointToPlane () {
	delete M_normal;
	}

private:

	double fitStep (double *T,const int32_t T_num,Matrix &R,Matrix &t,const std::vector<int32_t> &active);
	std::vector<int32_t> getInliers (double *T,const int32_t T_num,const Matrix &R,const Matrix &t,const double indist);
  
	// utility functions to compute normals from the model tree
	void computeNormal (const kdtree::KDTreeResultVector &neighbors,double *M_normal,const double flatness);
	double* computeNormals (const int32_t num_neighbors,const double flatness);
  
	// normals of model points
	double *M_normal;
};

#endif // ICP_POINT_TO_PLANE_H
