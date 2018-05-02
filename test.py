from elpigraph import computeElasticPrincipalCurve
import numpy as np

curve_data = np.genfromtxt('elpigraph/data/curve_data.csv', delimiter=',')
EPCurve = computeElasticPrincipalCurve(curve_data, 30)

print(curve_data)