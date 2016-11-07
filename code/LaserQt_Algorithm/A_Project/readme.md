#使用的是网上常见的boost扩展库，需要在打开项目前下载[boost库](https://sourceforge.net/projects/boost/files/boost/1.62.0/)。
两种方法使用库中的函数：

1、将源文件目录引入到编译器中；

2、将库文件包通过编译针对编译器生成lib文件插入到项目中[http://jingyan.baidu.com/article/a3aad71aa1ebe7b1fb009681.html](http://jingyan.baidu.com/article/a3aad71aa1ebe7b1fb009681.html)。


一个icp算法的简单实例，接口为icpPointToPlane类（icp算法的点对面模型）
用readfile函数读取路径中的数据，按照所给目标数据文件的格式读取的（如果格式不是这样就需要做预处理，使它使按照目标数据的格式排列，如果是二维数据，就需要重载了（还没有写）），然后由读取到的测试和目标数据M和T带入到接口类中计算，由icpPointToPlane类中的fit函数生成旋转和平移矩阵R和t，那么所需要做的误差分析就是M经过R、t变换得到的矩阵与T之间的差别（得到误差后应该怎么样？）。具体可看实例中的demo程序，其中fit函数中的外部值不好确定，就用默认值-1，而实际中应该是先对点云进行去噪再用fit函数求解变换矩阵。

1.png是未作任何处理的测试数据和目标数据用matlab绘出的效果图。
