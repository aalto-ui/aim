from setuptools import setup, find_packages

setup(
    name='aim_metrics',
    version='1.0',
    description='A collection of various pixel and segmentation based metrics for evaluating properties of user interface.',
    url='',
    author='Thomas Langerak, Yuxi Zhu, Akisato Kimura, Samuli De Pascale, Markku Laine',
    author_email='hello@thomaslangerak.nl, zhuyuxi1990@gmail.com, akisato@ieee.org, samuli.depascale@aalto.fi, markku.laine@aalto.fi',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'scipy',
        'Pillow',
        'scikit-image',
        'subprocess32',
    ],
    zip_safe=False
)
