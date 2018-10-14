from setuptools import setup, find_packages

setup(name='aim_segmentation',
      version='1.0',
      description='Tool for segmentation of images',
      author='Khushhall Chandra Mahajan, Janin Koch, Samuli De Pascale',
      author_email='',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'numpy',
          'scipy',
          'scikit-image'
      ],
      zip_safe=False)
