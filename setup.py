from setuptools import setup

setup(
  name='Bucketeer',
  version='0.1.0',
  author='Michal Garbacz',
  author_email='mich.garbacz+dev@gmail.com',
  packages=['bucketeer',],
  license='MIT License',
  description='Syncs a directory to a bucket in Amazon\'s S3 storage',
  long_description=open('README.md').read(),
  install_requires=[
    "boto == 2.6.0",
  ],
)

