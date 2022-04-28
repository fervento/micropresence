from setuptools import setup, find_packages
import micropresence

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name=micropresence.__project__,
    packages=find_packages(),
    version=micropresence.__version__,
    author=micropresence.__author__,
    author_email="fulvio@fervento.com",
    description=micropresence.__doc__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fervento/micropresence",
    entry_points = {
        "console_scripts": ['micropresence = micropresence.micropresence:main']
    },
    install_requires=[
        "sshuttle",
        "kubernetes"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: X?$ :: X#W",
        "Operating System :: OS Independent",
    ],
)