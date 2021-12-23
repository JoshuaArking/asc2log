from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("asc2log_c_opt.pyx", annotate=True)
)
