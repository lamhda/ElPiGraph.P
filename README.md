Description
===========

This package provides an Python implementation of the ElPiGraph algorithm. A
self-contained description of the algorithm is available
[here](https://github.com/auranic/Elastic-principal-graphs/blob/master/ElPiGraph_Methods.pdf)
or on this [arXiv paper](https://arxiv.org/abs/1804.07580)

A [R implementation](https://github.com/Albluca/ElPiGraph.R) of this algorithm is also available,
coded by [Luca Albergante](https://github.com/Albluca)

A native MATLAB implementation of the algorithm (coded by [Andrei
Zinovyev](https://github.com/auranic/) and [Evgeny
Mirkes](https://github.com/Mirkes)) is also
[available](https://github.com/auranic/Elastic-principal-graphs)

Citation
========

When using this package, please cite our preprint:

Albergante, L.  et al . Robust and Scalable  Learning of Data Manifold with Complex Topologies via ElPiGraph.
arXiv: [1804.07580](https://arxiv.org/abs/1804.07580) (2018)

Requirements
============

This code was tested with Python 3.6, the following packages are needed:

-	numpy
-	matplotlib
-   scipy
-   pip

Installation & Usage
====================

To install that package, clone this git, open a terminal on the root of the git folder and type:
```bash
pip install .
```

Or, without cloning, simply run the following command
```bash
pip install git+https://github.com/LouisFaure/ElPiGraph.P.git
```

Here is a notebook showing cases of [basic usage](elpigraph/docs/Basic%20usage.ipynb)
