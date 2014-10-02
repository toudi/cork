#-*- coding: utf-8
from setuptools import setup, find_packages

setup(
    name='cork',
    version=open('cork/version').read().strip(),
    packages=find_packages(),
    author="Mateusz Mikołajczyk",
    author_email="mikolajczyk.mateusz@gmail.com",
    install_requires=["flask-migrate", "flask-script", "flask-sqlalchemy"]
)
