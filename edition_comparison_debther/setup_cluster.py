from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("cluster_func_c.pyx" )
)
# python setup_cluster.py build_ext --inplace