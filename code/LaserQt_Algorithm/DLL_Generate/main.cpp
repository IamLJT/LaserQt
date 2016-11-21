#include <iostream>
#include <windows.h>

typedef void (*DLLFunc)(char*);	//	确定调用函数的形参

#define MAX 256

int main()
{
	DLLFunc dllFunc;
	//HINSTANCE hInstLibrary = LoadLibrary("D:\\研究生\\程序\\C++\\MFC\\testforicp\\icp\\TestDLL2\\Debug\\(ProjectDir)\\PointCloudAlgorithm.dll");

	//if (hInstLibrary == NULL)
	//{
	//	FreeLibrary(hInstLibrary);
	//}

	//dllFunc = (DLLFunc)GetProcAddress(hInstLibrary, "PointCloudDenoise");//第二个参数为要调用的函数名称

	//if (dllFunc == NULL)
 //   {
 //       FreeLibrary(hInstLibrary);
 //   }

	//dllFunc("C:\\Users\\Iam_luffy\\Documents\\GitHub\\LaserQt\\code\\LaserQt_Material\\测试数据.txt");
 //   FreeLibrary(hInstLibrary);

	char sPath[MAX];
	GetModuleFileName(NULL, sPath, MAX_PATH);

	strcat(sPath, "\\TempData.txt");

    return(1);
}