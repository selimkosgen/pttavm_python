from setuptools import setup, find_packages

setup(
    name="pttavm",
    version="0.1.3",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "requests",
        "xmltodict",
        "python-dateutil",
        "python-dotenv"
    ],
    python_requires=">=3.7",
)