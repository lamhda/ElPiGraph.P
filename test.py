from elpigraph import computeElasticPrincipalTree
from elpigraph import PlotPG
import numpy as np

tree_data = np.genfromtxt('elpigraph/data/tree_data.csv', delimiter=',')
EPTree = computeElasticPrincipalTree(tree_data, 20)


PlotPG(tree_data,EPTree)