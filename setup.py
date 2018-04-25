from setuptools import setup

setup(name='elpigraph',
      version='0.1',
      description='Python implementation of Elpigraph',
      url='https://github.com/LouisFaure/ElPiGraph.P',
      author='Alexi Martin',
      author_email='',
      packages=['functions','core_algorithm'],
      install_requires=[
          'numpy','matplotlib'
      ],
      zip_safe=False)
