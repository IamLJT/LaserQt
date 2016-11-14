1. The progrom implements DP
2. Requirements: 
  2.1 Python3
  2.2 The python modules need to be installed
  		-numpy(http://www.numpy.org/)
  		-matplotlib(http://matplotlib.org/)
  		-PIL(https://python-pillow.org/)
3. Source files:
	-dn.py
	-Y_Area.py
	-Z_Area.py
	-README.txt

4. This progrom does not need to be compiled.
5. Runing
	5.1 For training phase, run the following command:
		python dn.py -l e -f filenamelist -Y n -d networkfile -o outputfilename

		After trining phase, the program will create the following files:
			- stem-xy.pgm
			- stem-yz.pgm
			- stem-ay.txt
			- stem-az.txt
			- plot_stem-ay.png
			- plot_stem-az.png

	5.2 For testing phase, run the following command:
		python dn.py  -f filenamelist -d networkfile -o outputfilename
	5.3 The traininglist file  and testinglist file  and the images must be in the same directory.


