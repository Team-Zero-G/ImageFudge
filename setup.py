from setuptools import setup, find_packages
from setuptools.command.install import install


setup(name='ImageFudge',
      version='0.0.1',
      description='Image glitching library',
      license='MIT',
      author='William Patterson, Konstantin Farrell, Sean Sission',
      packages=find_packages(),
      package_data={},
      install_requires=['pillow'],
      entry_points={'console_scripts': ['imagefudge=imagefudge.__main__:main'],})
