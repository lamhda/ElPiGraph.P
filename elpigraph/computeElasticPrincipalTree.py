import numpy as np
from .computeElasticPrincipalGraph import computeElasticPrincipalGraph


def computeElasticPrincipalTree(data, NumNodes, newDim=None, drawPCAview=True,
                                 drawAccuracyComplexity=True, drawEnergy=True,
                                 Lambda=0.01, Mu=0.1, InitNodeP=None,
                                 InitEdges=None, ComputeMSEP=False,
                                 MaxBlockSize=100000, TrimmingRadius=np.inf,
                                 MaxNumberOfIterations=10, eps=0.01,
                                 verbose=True,nReps=1,ProbPoints=1):
    return computeElasticPrincipalGraph(data, NumNodes, newDim, drawPCAview,
                                        drawAccuracyComplexity, drawEnergy,
                                        Lambda, Mu, InitNodeP, InitEdges,
                                        np.array([["bisectedge"],["addnode2node"],["bisectedge"],["addnode2node"]]),
                                        np.array([["shrinkedge"],["removenode"]]), ComputeMSEP,
                                        MaxBlockSize, TrimmingRadius,
                                        MaxNumberOfIterations, eps, verbose, nReps,ProbPoints)