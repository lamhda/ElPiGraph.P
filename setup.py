from setuptools import setup

setup(name='elpigraph',
      version='0.9',
      description='Python implementation of Elpigraph',
      url='https://github.com/LouisFaure/ElPiGraph.P',
      author='Alexi Martin',
      author_email='',
      scripts=['core/funniest-joke'],
      packages=['elpigraph'],
      install_requires=[
          'numpy','matplotlib','scipy'
      ],
      zip_safe=False)
