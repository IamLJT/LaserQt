#ifndef __POINTCLOUDALGORITHM_H__
#define __POINTCLOUDALGORITHM_H__

extern "C" {
    void PointCloudDenoise(const char* path);
    void PointCloudFitting(const char* path, bool isFilter, const char* targetData);
}

#endif  // __POINTCLOUDALGORITHM_H__
