import os

from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as r_file:
    readme = r_file.read()

setup(name='cryptofy',
      version='1.1.0',
      description='Simple encryption/decryption functions for Python',
      long_description=readme,
      long_description_content_type='text/markdown',
      license='Apache 2.0',
      url='https://github.com/homedepot/cryptofy',
      author='Mike Phillipson',
      author_email='MICHAEL_PHILLIPSON1@homedepot.com',
      packages=[
          'cryptofy'
      ],
      scripts=[
          'bin/cryptofy'
      ],
      install_requires=[
          'pycryptodome'
      ],
      zip_safe=False)
