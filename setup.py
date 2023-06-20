"""Setup file for sentiment_analyzer package"""

from setuptools import setup

setup(
    name='sentiment_analyzer',
    version='0.0.1',
    packages=['sentiment_analyzer'],
    license='MIT',
    author='Ana Blanco Delgado',
    author_email='anablancodelgado@gmail.com',
    description='Python package for inspecting sentiment analysis datasets',
    install_requires=['pandas>=2.0.2',
                      'matplotlib>=3.7.1',
                      'wordcloud>=1.9.2']
)
