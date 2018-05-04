# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 10:56:58 2018

@author: Alexis Martin
"""
import numpy as np
from .PCA import PCA
from .core_algorithm.ElPrincGraph import ElPrincGraph
from .core_algorithm.MakeUniformElasticMatrix import MakeUniformElasticMatrix

# TODO : graphs
def computeElasticPrincipalGraph(data, NumNodes, newDim=None, drawPCAview=True,
                                 drawAccuracyComplexity=True, drawEnergy=True,
                                 Lambda=0.01, Mu=0.1, InitNodeP=None,
                                 InitEdges=None, growGrammar=None,
                                 shrinkGrammar=None, ComputeMSEP=False,
                                 MaxBlockSize=100000, TrimmingRadius=np.inf,
                                 MaxNumberOfIterations=10, eps=0.01,
                                 verbose=True,nReps=1,ProbPoints=1,Topo="None"):
    
    NodePositions = np.zeros((nReps+1, NumNodes, 3))
    ElasticMatrix = np.zeros((nReps+1, NumNodes, NumNodes))
    Edges = np.zeros((nReps + 1, 2, NumNodes - 1))
    if Topo=="Circle":
        Edges = np.zeros((nReps + 1, 2, NumNodes))


    for i in range(0, nReps):
        idx = np.random.uniform(0, 1, np.shape(data)[0]) < ProbPoints
        print("Iteration: ",i+1)
        NodeP = None
        EM = None
        if InitEdges is not None and InitNodeP is not None:
            NodeP = InitNodeP
            EM = MakeUniformElasticMatrix(InitEdges, Lambda, Mu)

        print("Performing PCA on the data")
        mv = data[idx, :].mean(axis=0)
        data_centered = data[idx, :] - mv
        vglobal, uglobal, explainedVariances = PCA(data_centered)
        if NodeP is not None:
            NodeP = NodeP - mv
            vg2, ug2, explainedV2 = PCA(NodeP)
        if newDim is not None:
            tmp = newDim.shape[0]
            if tmp == 1:
                indPC = np.arange(newDim[0])
            elif tmp == 2:
                indPC = np.arange(newDim[0], newDim[1])
            else:
                indPC = newDim
            perc = explainedVariances[indPC].sum()/explainedVariances.sum()*100
            print("Varaince retained in ", indPC.shape[0], " dimensions: ", perc)
            data_centered = uglobal[:, indPC]
            if NodeP is not None:
                NodeP = NodeP[:, indPC]
        else:
            indPC = np.arange(data[idx, :].shape[1])

        print("Computing EPG with ", NumNodes," nodes on ", sum(idx), " points and ", data.shape[1], " dimensions")
        NodePositions_tmp, ElasticMatrix_tmp = (
            ElPrincGraph(data_centered, NumNodes, Lambda, Mu, NodeP, EM,
                         growGrammar, shrinkGrammar, ComputeMSEP, MaxBlockSize,
                         TrimmingRadius, MaxNumberOfIterations, eps, verbose))

        if newDim is not None:
            NodePositions_tmp = np.dot(NodePositions_tmp, vglobal[:, indPC].T)
        Edges_tmp = np.vstack(np.triu(ElasticMatrix_tmp, 1).nonzero())
        NodePositions_tmp += mv
        NodePositions[i, :, :] = NodePositions_tmp
        Edges[i, :, :] = Edges_tmp
        ElasticMatrix[i, :, :] = ElasticMatrix_tmp


    if nReps > 1:
        print("Constructing average graph")
        datashape = NodePositions.shape
        npoints = datashape[0] * datashape[1]
        finalNodes = NodePositions[0, :, :]
        for i in range(1, datashape[0]-1):
            finalNodes = np.append(finalNodes, NodePositions[i, :, :], axis=0)
        #finalNodes = NodePositions.reshape(npoints, datashape[2])
        print("Performing PCA on all computed nodes")

        print("Computing EPG with ", NumNodes, " nodes on ", npoints, " points and ", datashape[2], " dimensions")
        NodePositions_tmp, ElasticMatrix_tmp = (
            ElPrincGraph(finalNodes, NumNodes, Lambda, Mu, NodeP, EM,
                     growGrammar, shrinkGrammar, ComputeMSEP, MaxBlockSize,
                     TrimmingRadius, MaxNumberOfIterations, eps, verbose))

        Edges_tmp = np.vstack(np.triu(ElasticMatrix_tmp, 1).nonzero())
        NodePositions[nReps, :, :] = NodePositions_tmp
        Edges[nReps, :, :] = Edges_tmp
        ElasticMatrix[nReps, :, :] = ElasticMatrix_tmp
        return NodePositions, ElasticMatrix, Edges

    else:
        return np.expand_dims(NodePositions_tmp,axis=0), \
               np.expand_dims(ElasticMatrix_tmp,axis=0), \
               np.expand_dims(Edges_tmp,axis=0)
