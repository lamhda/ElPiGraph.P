def computeElasticPrincipalCircle(data, NumNodes, newDim=None,
                                  drawPCAview=True,
                                  drawAccuracyComplexity=True, drawEnergy=True,
                                  Lambda=0.01, Mu=0.1, ComputeMSEP=False,
                                  MaxBlockSize=100000, TrimmingRadius=np.inf,
                                  MaxNumberOfIterations=10, eps=0.01,
                                  verbose=True):
    NodeP = np.zeros((4, data.shape[1]))
    v, u, s = PCA(data)
    mn = data.mean(axis=0)
    v1 = v[:, 0]/np.linalg.norm(v[:, 0])
    v2 = v[:, 1]/np.linalg.norm(v[:, 1])
    st1 = np.std(u[:, 0], ddof=1)
    st2 = np.std(u[:, 1], ddof=1)
    NodeP[0, :] = mn - np.dot(st1, v1.T) - np.dot(st2, v2.T)
    NodeP[1, :] = mn - np.dot(st1, v1.T) + np.dot(st2, v2.T)
    NodeP[2, :] = mn + np.dot(st1, v1.T) + np.dot(st2, v2.T)
    NodeP[3, :] = mn + np.dot(st1, v1.T) - np.dot(st2, v2.T)
    ed = np.array([[0, 1], [2, 3], [1, 2], [3, 0]])
    return EPG.computeElasticPrincipalGraph(data, NumNodes, newDim,
                                            drawPCAview,
                                            drawAccuracyComplexity,
                                            drawEnergy, Lambda,
                                            Mu, NodeP, ed,
                                            np.array([["bisectedge"]]),
                                            np.array([]), ComputeMSEP,
                                            MaxBlockSize, TrimmingRadius,
                                            MaxNumberOfIterations, eps,
                                            verbose)


def computeElasticPrincipalCurve(data, NumNodes, newDim=None, drawPCAview=True,
                                 drawAccuracyComplexity=True, drawEnergy=True,
                                 Lambda=0.01, Mu=0.1, InitNodeP=None,
                                 InitEdges=None, ComputeMSEP=False,
                                 MaxBlockSize=100000, TrimmingRadius=np.inf,
                                 MaxNumberOfIterations=10, eps=0.01,
                                 verbose=True):
    return computeElasticPrincipalGraph(data, NumNodes, newDim, drawPCAview,
                                        drawAccuracyComplexity, drawEnergy,
                                        Lambda, Mu, InitNodeP, InitEdges,
                                        np.array([["bisectedge"]]),
                                        np.array([]), ComputeMSEP,
                                        MaxBlockSize, TrimmingRadius,
                                        MaxNumberOfIterations, eps, verbose)


def computeElasticPrincipalGraph(data, NumNodes, newDim=None, drawPCAview=True,
                                 drawAccuracyComplexity=True, drawEnergy=True,
                                 Lambda=0.01, Mu=0.1, InitNodeP=None,
                                 InitEdges=None, growGrammar=None,
                                 shrinkGrammar=None, ComputeMSEP=False,
                                 MaxBlockSize=100000, TrimmingRadius=np.inf,
                                 MaxNumberOfIterations=10, eps=0.01,
                                 verbose=True):
    NodeP = None
    EM = None
    if InitEdges is not None and InitNodeP is not None:
        NodeP = InitNodeP
        EM = MakeUniformElasticMatrix(InitEdges, Lambda, Mu)
    mv = data.mean(axis=0)
    data_centered = data - mv
    vglobal, uglobal, explainedVariances = PCAV.PCA(data_centered)
    if NodeP is not None:
        NodeP = NodeP - mv
        vg2, ug2, explainedV2 = PCAV.PCA(NodeP)
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
        indPC = np.arange(data.shape[1])

    NodePositions, ElasticMatrix = (
        ElPrincGraph(data_centered, NumNodes, Lambda, Mu, NodeP, EM,
                     growGrammar, shrinkGrammar, ComputeMSEP, MaxBlockSize,
                     TrimmingRadius, MaxNumberOfIterations, eps, verbose))

    if newDim is not None:
        NodePositions = np.dot(NodePositions, vglobal[:, indPC].T)
    Edges = np.vstack(np.triu(ElasticMatrix, 1).nonzero())
    NodePositions += mv
    return NodePositions, ElasticMatrix, Edges


def computeRobustElasticPrincipalGraph(data, NumNodes,  TrimmingRadius,
                                       newDim=None, drawPCAview=True,
                                       drawAccuracyComplexity=True,
                                       drawEnergy=True, Lambda=0.01, Mu=0.1,
                                       InitNodeP=None, InitEdges=None,
                                       growGrammar=None, shrinkGrammar=None,
                                       ComputeMSEP=False, MaxBlockSize=100000,
                                       MaxNumberOfIterations=10, eps=0.01,
                                       verbose=True):
    nodeP = np.zeros((2, data.shape[1]))
    ed = np.array([[0, 1]])
    NumberOfSamples = np.floor(data.shape[0]/10)
    if NumberOfSamples > 1000:
        NumberOfSamples = 1000
    sampling = np.random.permutation(range(data.shape[0]))[:NumberOfSamples]
    

