# setup.py
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

config = dict(name='CloudHarvestCLI',
              version='0.1.0',
              description='This is the Command Line Interface for CloudHarvest.',
              author='Cloud Harvest, Fiona June Leathers',
              url='https://github.com/Cloud-Harvest/CloudHarvestCLI',
              packages=find_packages(include=['CloudHarvestCLI']),
              install_requires=requirements,
              classifiers=[
                  'Development Status :: 3 - Alpha',
                  'Intended Audience :: Developers',
                  'License :: OSI Approved :: MIT License',
                  'Programming Language :: Python :: 3.12',
              ])

setup(**config)
