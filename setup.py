from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pttavm-python",
    version="0.1.5",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "requests>=2.25.0",
        "xmltodict>=0.12.0",
        "python-dateutil>=2.8.0",
        "python-dotenv>=0.15.0"
    ],
    python_requires=">=3.7",
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov",
            "black",
            "isort",
            "flake8",
            "twine",
            "build"
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Natural Language :: Turkish",
    ],
    description="PTT AVM API client library for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Selim Kosgen",
    author_email="selimkosgen1999@gmail.com",
    url="https://github.com/selimkosgen/pttavm_python",
    project_urls={
        "Bug Tracker": "https://github.com/selimkosgen/pttavm_python/issues",
        "Documentation": "https://github.com/selimkosgen/pttavm_python/wiki",
        "Source Code": "https://github.com/selimkosgen/pttavm_python",
    },
    keywords="ptt avm api client soap ecommerce marketplace",
)