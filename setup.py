from setuptools import setup, find_packages

setup(
    name='slackbotpry',
    version='0.0.1',
    packages=find_packages(exclude=['tests']),
    author='rokurosatp, obsproth',
    url='https://github.com/rokurosatp/slackbotpry',
    install_requires=['slackclient>=1.0.0',],
)

