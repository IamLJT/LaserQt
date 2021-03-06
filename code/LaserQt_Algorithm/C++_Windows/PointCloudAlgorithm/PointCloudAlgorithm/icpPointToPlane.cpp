/*
Copyright 2011. All rights reserved.
Institute of Measurement and Control Systems
Karlsruhe Institute of Technology, Germany

Authors: Andreas Geiger

libicp is free software; you can redistribute it and/or modify it under the
terms of the GNU General Public License as published by the Free Software
Foundation; either version 2 of the License, or any later version.

libicp is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
libicp; if not, write to the Free Software Foundation, Inc., 51 Franklin
Street, Fifth Floor, Boston, MA 02110-1301, USA 
*/

#include "icpPointToPlane.h"
#include "readfile.h"

using namespace std;

// Also see (3d part): "Linear Least-Squares Optimization for Point-to-Plane ICP Surface Registration" (Kok-Lim Low)
double IcpPointToPlane::fitStep (double *T,const int32_t T_num,Matrix &R,Matrix &t,const std::vector<int32_t> &active) {

	// kd tree query + result
	std::vector<float>	query(dim);
	kdtree::KDTreeResultVector result;

	// init matrix for point correspondences
	Matrix p_m(active.size(),dim); // model
	Matrix p_t(active.size(),dim); // template
  
	// dimensionality 2
	if (dim==2) {

	// extract matrix and translation vector
	double r00 = R.val[0][0]; double r01 = R.val[0][1];
	double r10 = R.val[1][0]; double r11 = R.val[1][1];
	double t0  = t.val[0][0]; double t1  = t.val[1][0];

	// init A and b
	Matrix A(active.size(),3);
	Matrix b(active.size(),1);

	// establish correspondences
	for (int32_t i=0; i<active.size(); i++) {

		// get index of active point
		int32_t idx = active[i];

		// transform point according to R|t
		query[0] = r00*T[idx*2+0] + r01*T[idx*2+1] + t0;
		query[1] = r10*T[idx*2+0] + r11*T[idx*2+1] + t1;

		// search nearest neighbor
		M_tree->n_nearest(query,1,result);

		// model point
		double dx = M_tree->the_data[result[0].idx][0];
		double dy = M_tree->the_data[result[0].idx][1];

		// model point normal
		double nx = M_normal[result[0].idx*2+0];
		double ny = M_normal[result[0].idx*2+1];

		// template point
		double sx = query[0];
		double sy = query[1];

		// setup least squares system
		A.val[i][0] = ny*sx-nx*sy;
		A.val[i][1] = nx;
		A.val[i][2] = ny;
		b.val[i][0] = nx*dx+ny*dy-nx*sx-ny*sy;    
	}

	// linear least square matrices
	Matrix A_ = ~A*A;
	Matrix b_ = ~A*b;

	// solve linear system
	if (b_.solve(A_)) {

		// rotation matrix
		Matrix R_ = Matrix::eye(2);
		R_.val[0][1] = -b_.val[0][0];
		R_.val[1][0] = +b_.val[0][0];

		// orthonormalized rotation matrix
		Matrix U,W,V;
		R_.svd(U,W,V);
		R_ = U*~V;  

		// translation vector
		Matrix t_(2,1);
		t_.val[0][0] = b_.val[1][0];
		t_.val[1][0] = b_.val[2][0];

		// compose: R|t = R_|t_ * R|t
		R = R_*R;
		t = R_*t+t_;
		return max((R_-Matrix::eye(2)).l2norm(),t_.l2norm());
	}
   
	// dimensionality 3
	} else {
    
	// extract matrix and translation vector
	double r00 = R.val[0][0]; double r01 = R.val[0][1]; double r02 = R.val[0][2];
	double r10 = R.val[1][0]; double r11 = R.val[1][1]; double r12 = R.val[1][2];
	double r20 = R.val[2][0]; double r21 = R.val[2][1]; double r22 = R.val[2][2];
	double t0  = t.val[0][0]; double t1  = t.val[1][0]; double t2  = t.val[2][0];

	// init A and b
	Matrix A(active.size(),6);
	Matrix b(active.size(),1);

	// establish correspondences
	for (int32_t i=0; i<active.size(); i++) {

		// get index of active point
		int32_t idx = active[i];

		// transform point according to R|t
		query[0] = r00*T[idx*3+0] + r01*T[idx*3+1] + r02*T[idx*3+2] + t0;
		query[1] = r10*T[idx*3+0] + r11*T[idx*3+1] + r12*T[idx*3+2] + t1;
		query[2] = r20*T[idx*3+0] + r21*T[idx*3+1] + r22*T[idx*3+2] + t2;

		// search nearest neighbor
		M_tree->n_nearest(query,1,result);

		// model point
		double dx = M_tree->the_data[result[0].idx][0];
		double dy = M_tree->the_data[result[0].idx][1];
		double dz = M_tree->the_data[result[0].idx][2];

		// model point normal
		double nx = M_normal[result[0].idx*3+0];
		double ny = M_normal[result[0].idx*3+1];
		double nz = M_normal[result[0].idx*3+2];

		// template point
		double sx = query[0];
		double sy = query[1];
		double sz = query[2];

		// setup least squares system
		A.val[i][0] = nz*sy-ny*sz;
		A.val[i][1] = nx*sz-nz*sx;
		A.val[i][2] = ny*sx-nx*sy;
		A.val[i][3] = nx;
		A.val[i][4] = ny;
		A.val[i][5] = nz;
		b.val[i][0] = nx*dx+ny*dy+nz*dz-nx*sx-ny*sy-nz*sz;    
	}

	// linear least square matrices
	Matrix A_ = ~A*A;
	Matrix b_ = ~A*b;

	// solve linear system
	if (b_.solve(A_)) {

		// rotation matrix
		Matrix R_ = Matrix::eye(3);
		R_.val[0][1] = -b_.val[2][0];
		R_.val[1][0] = +b_.val[2][0];
		R_.val[0][2] = +b_.val[1][0];
		R_.val[2][0] = -b_.val[1][0];
		R_.val[1][2] = -b_.val[0][0];
		R_.val[2][1] = +b_.val[0][0];

		// orthonormalized rotation matrix
		Matrix U,W,V;
		R_.svd(U,W,V);
		R_ = U*~V;  

		// translation vector
		Matrix t_(3,1);
		t_.val[0][0] = b_.val[3][0];
		t_.val[1][0] = b_.val[4][0];
		t_.val[2][0] = b_.val[5][0];

		// compose: R|t = R_|t_ * R|t
		R = R_*R;
		t = R_*t+t_;
		return max((R_-Matrix::eye(3)).l2norm(),t_.l2norm());
	}
	}
  
	// failure
	return 0;
}

std::vector<int32_t> IcpPointToPlane::getInliers (double *T,const int32_t T_num,const Matrix &R,const Matrix &t,const double indist) {
  
	// init inlier vector + query point + query result
	vector<int32_t>            inliers;
	std::vector<float>         query(dim);
	kdtree::KDTreeResultVector neighbor;
  
	// dimensionality 2
	if (dim==2) {
  
	// extract matrix and translation vector
	double r00 = R.val[0][0]; double r01 = R.val[0][1];
	double r10 = R.val[1][0]; double r11 = R.val[1][1];
	double t0  = t.val[0][0]; double t1  = t.val[1][0];

	// check for all points if they are inliers
	for (int32_t i=0; i<T_num; i++) {

		// transform point according to R|t
		double sx = r00*T[i*2+0] + r01*T[i*2+1]; query[0] = sx;
		double sy = r10*T[i*2+0] + r11*T[i*2+1]; query[1] = sy;

		// search nearest neighbor
		M_tree->n_nearest(query,1,neighbor);

		// model point
		double dx = M_tree->the_data[neighbor[0].idx][0];
		double dy = M_tree->the_data[neighbor[0].idx][1];

		// model point normal
		double nx = M_normal[neighbor[0].idx*2+0];
		double ny = M_normal[neighbor[0].idx*2+1];

		// check if it is an inlier
		if ((sx-dx)*nx+(sy-dy)*ny<indist)
		inliers.push_back(i);
	}
    
	// dimensionality 3
	} else {
    
	// extract matrix and translation vector
	double r00 = R.val[0][0]; double r01 = R.val[0][1]; double r02 = R.val[0][2];
	double r10 = R.val[1][0]; double r11 = R.val[1][1]; double r12 = R.val[1][2];
	double r20 = R.val[2][0]; double r21 = R.val[2][1]; double r22 = R.val[2][2];
	double t0  = t.val[0][0]; double t1  = t.val[1][0]; double t2  = t.val[2][0];

	// check for all points if they are inliers
	for (int32_t i=0; i<T_num; i++) {

		// transform point according to R|t
		double sx = r00*T[i*3+0] + r01*T[i*3+1] + r02*T[i*3+2] + t0; query[0] = sx;
		double sy = r10*T[i*3+0] + r11*T[i*3+1] + r12*T[i*3+2] + t1; query[1] = sy;
		double sz = r20*T[i*3+0] + r21*T[i*3+1] + r22*T[i*3+2] + t2; query[2] = sz;

		// search nearest neighbor
		M_tree->n_nearest(query,1,neighbor);

		// model point
		double dx = M_tree->the_data[neighbor[0].idx][0];
		double dy = M_tree->the_data[neighbor[0].idx][1];
		double dz = M_tree->the_data[neighbor[0].idx][2];

		// model point normal
		double nx = M_normal[neighbor[0].idx*3+0];
		double ny = M_normal[neighbor[0].idx*3+1];
		double nz = M_normal[neighbor[0].idx*3+2];

		// check if it is an inlier
		if ((sx-dx)*nx+(sy-dy)*ny+(sz-dz)*nz<indist)
		inliers.push_back(i);
	}
	}
  
	// return vector with inliers
	return inliers;
}

void IcpPointToPlane::computeNormal (const kdtree::KDTreeResultVector &neighbors,double *M_normal,const double flatness) {
  
	// dimensionality 2
	if (dim==2) {
    
	// extract neighbors
	Matrix P(neighbors.size(),2);
	Matrix mu(1,2);
	for (int32_t i=0; i<neighbors.size(); i++) {
		double x = M_tree->the_data[neighbors[i].idx][0];
		double y = M_tree->the_data[neighbors[i].idx][1];
		P.val[i][0] = x;
		P.val[i][1] = y;
		mu.val[0][0] += x;
		mu.val[0][1] += y;
	}

	// zero mean
	mu       = mu/(double)neighbors.size();
	Matrix Q = P - Matrix::ones(neighbors.size(),1)*mu;

	// principal component analysis
	Matrix H = ~Q*Q;
	Matrix U,W,V;
	H.svd(U,W,V);

	// normal
	M_normal[0] = U.val[0][1];
	M_normal[1] = U.val[1][1];
  
	// dimensionality 3
	} else {
    
	// extract neighbors
	Matrix P(neighbors.size(),3);
	Matrix mu(1,3);
	for (int32_t i=0; i<neighbors.size(); i++) {
		double x = M_tree->the_data[neighbors[i].idx][0];
		double y = M_tree->the_data[neighbors[i].idx][1];
		double z = M_tree->the_data[neighbors[i].idx][2];
		P.val[i][0] = x;
		P.val[i][1] = y;
		P.val[i][2] = z;
		mu.val[0][0] += x;
		mu.val[0][1] += y;
		mu.val[0][2] += z;
	}

	// zero mean
	mu       = mu/(double)neighbors.size();
	Matrix Q = P - Matrix::ones(neighbors.size(),1)*mu;

	// principal component analysis
	Matrix H = ~Q*Q;
	Matrix U,W,V;
	H.svd(U,W,V);

	// normal
	M_normal[0] = U.val[0][2];
	M_normal[1] = U.val[1][2];
	M_normal[2] = U.val[2][2];
	}
}

double* IcpPointToPlane::computeNormals (const int32_t num_neighbors,const double flatness) {
	double *M_normal = (double*)malloc(M_tree->N*dim*sizeof(double));
	kdtree::KDTreeResultVector neighbors;
	for (int32_t i=0; i<M_tree->N; i++) {
	M_tree->n_nearest_around_point(i,0,num_neighbors,neighbors);
	if (dim==2) computeNormal(neighbors,M_normal+i*2,flatness);
	else        computeNormal(neighbors,M_normal+i*3,flatness);
	}
	return M_normal;
}

vector<int> IcpPointToPlane::getNearest(int index, double r, vector<bool>& isvisited) {
	kdtree::KDTreeResultVector neighbors;
	M_tree->r_nearest_around_point(index, 0, r, neighbors);
	// 这里的neighbours中存的序号是M_tree里的序号
	vector<int> res;
	for (int i = 0; i < neighbors.size(); ++i) {
		if (isvisited[neighbors[i].idx])
			continue;
		res.push_back(neighbors[i].idx);
	}
	return res;
}

vector<vector<double>> IcpPointToPlane::getcluster(int min_p, double r, vector<bool>& isvisited) {
	// min_p表示密度邻域值，表示是否能允许新的点加入
	// r为半径邻域值，即通过r去寻找邻域点
	int num = isvisited.size();
	vector<vector<double>> res;
	for (int i = 0; i < num; ++i) {
		if (isvisited[i]) continue;
		vector<double> temp;
		queue<int> q; // 放入遍历到的数按队列依次
		//temp.push_back(M_tree->the_data[i][0]);
		//temp.push_back(M_tree->the_data[i][1]);
		//temp.push_back(M_tree->the_data[i][2]);
		q.push(i);
		while (q.size()) {
			int t = q.front();
			q.pop();
			//if (isvisited[t]) continue;
			isvisited[t] = 1; // 这里究竟是符合条件后才设置已访问呢？
			vector<int> tmp_p = getNearest(t, r, isvisited);
			if (tmp_p.size() > min_p) {
				temp.push_back(M_tree->the_data[t][0]);
				temp.push_back(M_tree->the_data[t][1]);
				temp.push_back(M_tree->the_data[t][2]);
				for (int j = 0; j < tmp_p.size(); ++j) {
					q.push(tmp_p[j]);
					//temp.push_back(M_tree->the_data[tmp_p[j]][0]);
					//temp.push_back(M_tree->the_data[tmp_p[j]][1]);
					//temp.push_back(M_tree->the_data[tmp_p[j]][2]);
					isvisited[tmp_p[j]] = 1;
				}
			}
			else {
				isvisited[t] = 0;
			}
		}
		if (temp.size() > 5 * dim)
			res.push_back(temp);

		double *m_temp = new double[temp.size()];
		int k = 0;
		for (auto c : temp)
			m_temp[k++] = c;
		const int MAX = 256;
		char sPath[MAX];
		getcwd(sPath, MAX_PATH);

		strcat(sPath, "\\NewGrid_TempData2.txt");
		//WriteFile(sPath, M0, num, dim);
		WriteFile(sPath, m_temp, temp.size() / dim, dim);
	}
	return res;
}