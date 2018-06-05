from setuptools import setup
try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()

setup(name='elpigraph',
      version='0.91',
      description='Python implementation of Elpigraph',
      long_description=read_md('README.md'),
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
