# -*- coding: utf-8 -*-
"""
@author: Louis Faure
"""
import numpy as np
import matplotlib.pyplot as plt
from .PCA import PCA
plt.style.use('ggplot')


def PlotPG(data,EPC):
    EPCidx = EPC[0].shape[0] - 1
    print(EPCidx)
    # Perform PCA on the nodes
    mv = EPC[0][EPCidx].mean(axis=0)
    data_centered = EPC[0][EPCidx] - mv
    vglobal, uglobal, _ = PCA(data_centered)

    # Rotate the data using eigenvectors
    RotData = np.dot((data - mv),vglobal)

    # Plot results
    plt.figure()
    plt.scatter(RotData[:,0],RotData[:,1],s=10,c="b",alpha= 0.5)

    for i in range(0,EPCidx):
        Rotnodes = np.dot((EPC[0][i] - mv),vglobal)
        for j in range(0, len(EPC[2][i][1, :])):
            plt.plot(Rotnodes[EPC[2][i][:, j].astype(int), 0], Rotnodes[EPC[2][i][:, j].astype(int), 1], "k",alpha=0.3)

    plt.plot(uglobal[:,0],uglobal[:,1], 'ro')
    for i in range(0,len(EPC[2][EPCidx][1,:])):
        plt.plot(uglobal[EPC[2][EPCidx][:,i].astype(int),0],uglobal[EPC[2][EPCidx][:,i].astype(int),1],"r")

    plt.show()