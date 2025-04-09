from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="zmapsdk",
    version="0.1.0",
    author="Atilla",
    author_email="attilla@tuta.io",
    description="Python SDK for the ZMap network scanner",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/atiilla/zmapsdk",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12", 
        "Programming Language :: Python :: 3.13",
        "Operating System :: POSIX :: Linux",
        "Topic :: System :: Networking",
        "Topic :: Security",
    ],
    python_requires=">=3.6",
    install_requires=[],
) 