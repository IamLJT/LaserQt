#include <iostream>
#include <windows.h>

typedef void (*DLLFunc)(char*);	//	ȷ�����ú������β�

#define MAX 256

int main()
{
	DLLFunc dllFunc;
	//HINSTANCE hInstLibrary = LoadLibrary("D:\\�о���\\����\\C++\\MFC\\testforicp\\icp\\TestDLL2\\Debug\\(ProjectDir)\\PointCloudAlgorithm.dll");

	//if (hInstLibrary == NULL)
	//{
	//	FreeLibrary(hInstLibrary);
	//}

	//dllFunc = (DLLFunc)GetProcAddress(hInstLibrary, "PointCloudDenoise");//�ڶ�������ΪҪ���õĺ�������

	//if (dllFunc == NULL)
 //   {
 //       FreeLibrary(hInstLibrary);
 //   }

	//dllFunc("C:\\Users\\Iam_luffy\\Documents\\GitHub\\LaserQt\\code\\LaserQt_Material\\��������.txt");
 //   FreeLibrary(hInstLibrary);

	char sPath[MAX];
	GetModuleFileName(NULL, sPath, MAX_PATH);

	strcat(sPath, "\\TempData.txt");

    return(1);
}