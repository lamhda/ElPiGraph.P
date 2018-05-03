from setuptools import setup

setup(name='elpigraph',
      version='0.91',
      description='Python implementation of Elpigraph',
      url='https://github.com/LouisFaure/ElPiGraph.P',
      author='Alexi Martin',
      author_email='',
      packages=['elpigraph.core_algorithm','elpigraph'],
      package_dir={'elpigraph': 'elpigraph'},
      package_data={'elpigraph': ['data/*.csv']},
      install_requires=[
          'numpy','matplotlib','scipy'
      ],
      zip_safe=False)
