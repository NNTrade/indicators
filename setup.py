import setuptools
import os
from pathlib import Path
import pkg_resources

with open("README.md", "r") as fh:
    long_description = fh.read()

def get_req_files(file:str):
    file_path = os.path.join(Path('.'),file)
    with open(file_path) as requirements_txt:
        return [str(requirement) for requirement in pkg_resources.parse_requirements(requirements_txt)]

def get_requirements():
    ret_requires = []
    for req_txt in get_req_files("requirements.txt"):
        ret_requires.append(req_txt)
    return ret_requires

lib = "NNTrade.indicators"
packages = [lib] + [f"{lib}.{pkg}" for pkg in setuptools.find_packages(where="src")]
setuptools.setup(
    name=lib,
    version="2.0.1",
    author="InsonusK",
    author_email="insonus.k@gmail.com",
    description="Framework with indicators for trading robots",
    long_description=long_description,
    url="https://github.com/NNTrade/indicators",
    packages=packages,
    package_dir={lib:'src'},
    install_requires=get_requirements(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)