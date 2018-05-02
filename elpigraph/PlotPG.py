# -*- coding: utf-8 -*-
"""
@author: Louis Faure
"""
import numpy as np
import matplotlib.pyplot as plt
from .PCAView import PCA
plt.style.use('ggplot')

def PlotPG(data,EPC):
	# Perform PCA on the nodes
	mv = EPC[0].mean(axis=0)
	data_centered = EPC[0] - mv
	vglobal, uglobal, explainedVariances = PCA(data_centered)

	# Rotate the data using eigenvectors
	RotData = np.dot((data - mv),vglobal)

	# PLot results
	plt.figure()
	plt.scatter(RotData[:,0],RotData[:,1],s=10,c="b",alpha= 0.5)
	plt.plot(uglobal[:,0],uglobal[:,1], 'ro')
	for i in range(0,len(EPC[2][1,:])):
	    plt.plot(uglobal[EPC[2][:,i],0],uglobal[EPC[2][:,i],1],"r")

	plt.show()