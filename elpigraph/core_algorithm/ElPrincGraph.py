# -*- coding: utf-8 -*-
"""
Created on Fri Jan 26 10:48:28 2018

@author: Alexis Martin
"""
import numpy as np
from .MakeUniformElasticMatrix import MakeUniformElasticMatrix
from . import ApplyOptimalGraphGrammarOperation as ao
from elpigraph.PCA import PCA


# TODO add report
def ElPrincGraph(X, NumNodes, Lambda, Mu, InitNodePosition=None,
                 InitElasticMatrix=None, growGrammar=None, shrinkGrammar=None,
                 ComputeMSEP=False, MaxBlockSize=100000,
                 TrimmingRadius=np.inf, MaxNumberOfIterations=10,
                 eps=0.01, verbose=True):
    if growGrammar is None:
        growGrammar = np.array([["bisectedge", "addnode2node"],
                                ["bisectedge", "addnode2node"]])
    if shrinkGrammar is None:
        shrinkGrammar = np.array([["shrinkedge", "removenode"]])
    NodeP = InitNodePosition
    em = InitElasticMatrix
    if em is not None and np.all(em != em.T):
        raise ValueError("Elastic Matrix must be square and symmetric")
    if NodeP is not None:
        CurrentNumberOfNodes = NodeP.shape[0]
    else:
        CurrentNumberOfNodes = 0
    if em is None:
        if CurrentNumberOfNodes == 0:
            edges = np.array([[0, 1]])
        else:
            edges = np.vstack((np.arange(CurrentNumberOfNodes-1),
                               np.arange(1, CurrentNumberOfNodes))).T
        em = MakeUniformElasticMatrix(edges, Lambda, Mu)
    if CurrentNumberOfNodes == 0:
        CurrentNumberOfNodes = em.shape[0]

        ## Louis Modification
        mv = X.mean(axis=0)
        data_centered = X - mv
        vglobal, uglobal, explainedVariances = PCA(data_centered)
        PC1 = uglobal[:,0]

        mn = np.mean(PC1)
        st = np.std(PC1)

        NodeP = np.dot(np.linspace(mn - st, mn + st, CurrentNumberOfNodes).reshape(2,1), vglobal[:,0].reshape(1,3))
        #NodeP = NodeP+mv.reshape(3,1)

        ## OLD CODE
        _, _, v = np.linalg.svd(X)
        v = abs(v[0,])
        mn = X.mean(axis=0)
        st = np.std((X * v).sum(axis=1), ddof=1)
        delta = 2 * st / (CurrentNumberOfNodes - 1)
        NodeP2 = ((mn - st * v) +
                 ((delta * range(CurrentNumberOfNodes))[np.newaxis].T * v))


    CurrentNumberOfNodes = NodeP.shape[0]
    UR = em.diagonal()
    if (UR > 0).sum() == 0:
        em = em + np.diag(Mu*np.ones((CurrentNumberOfNodes)))
    # if verbose:
    #     print('BARCODE\tENERGY\tNNODES\tNEDGES\tNRIBS\tNSTARS' +
    #           '\tNRAYS\tNRAYS2\tMSE MSEP\tFVE\tFVEP\tUE\tUR\tURN\tURN2\tURSD')
    if growGrammar.shape[0] <= shrinkGrammar.shape[0]:
        raise ValueError("The tree cannot grow if less growing grammar than " +
                         "shrinking grammar.")

    print("NODE:")
    while NodeP.shape[0] < NumNodes:
        print(NodeP.shape[0],end=" ")
        for k in range(growGrammar.shape[0]):
            NodeP, em, partition, dists, ElasticEnergy, MSE, EP, RP = (
                    ao.ApplyOptimalGraphGrammarOperation(X, NodeP, em,
                                                         growGrammar[k],
                                                         MaxBlockSize, verbose,
                                                         TrimmingRadius,
                                                         MaxNumberOfIterations,
                                                         eps))
        for k in range(shrinkGrammar.shape[0]):
            NodeP, em, partition, dists, ElasticEnergy, MSE, EP, RP = (
                    ao.ApplyOptimalGraphGrammarOperation(X, NodeP, em,
                                                         shrinkGrammar[k],
                                                         MaxBlockSize, verbose,
                                                         TrimmingRadius,
                                                         MaxNumberOfIterations,
                                                         eps))
    if verbose:
        print("",end="\n")
        print("E=", ElasticEnergy, ", MSE=", MSE, ", EP=", EP, ", RP=", RP)
    print("Done")
    return NodeP, em
