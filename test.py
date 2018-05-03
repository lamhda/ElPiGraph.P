from elpigraph import computeElasticPrincipalCurve
from elpigraph import computeElasticPrincipalCircle
from elpigraph import computeElasticPrincipalTree
from elpigraph import PlotPG
import numpy as np

tree_data = np.genfromtxt('elpigraph/data/tree_data.csv', delimiter=',')
EPTree = computeElasticPrincipalTree(tree_data, 20)

#curve_data = np.genfromtxt('elpigraph/data/curve_data.csv', delimiter=',')
#EPCurve = computeElasticPrincipalCurve(curve_data, 10,nReps=10,ProbPoints=0.9)

#print(curve_data)

PlotPG(tree_data,EPTree)