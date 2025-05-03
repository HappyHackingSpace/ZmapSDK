from setuptools import find_packages, setup

with open("README.md", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="zmapsdk",
    version="0.1.3",
    description="Python SDK for the ZMap network scanner with REST API",
    author="ZMap Team",
    author_email="info@zmap.io",
    url="https://github.com/zmap/zmapsdk",
    packages=find_packages(),
    install_requires=[
        "pydantic>=1.8.0,<2.0.0",  # For data validation
        "fastapi>=0.68.0",  # For REST API
        "uvicorn>=0.15.0",  # For serving the API
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "black>=21.5b2",
            "isort>=5.9.1",
            "mypy>=0.812",
        ],
    },
    entry_points={
        "console_scripts": [
            "zmapsdk=zmapsdk.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Internet",
        "Topic :: Security",
        "Topic :: System :: Networking",
    ],
    python_requires=">=3.7",
)
