from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

requirements_path = path.join(path.dirname(path.realpath(__file__)), 'requirements.txt')
install_requires = []
if path.isfile(requirements_path):
    with open(requirements_path) as f:
        install_requires = f.read().splitlines()
        print(install_requires)

setup(
    name='glu-pictures-tools',
    version='0.0.1',
    description="Pictures tools",
    author="Guillaume Lucazeau (Advanced Schema)",
    author_email="glucazeau.prestataire@idkids.com",
    packages=find_packages(exclude='tests'),
    py_modules=['picture', 'find_duplicates', 'common'],
    install_requires=[
        install_requires
    ],
    include_package_data=False,
)
