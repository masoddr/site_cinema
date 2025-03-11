from setuptools import setup, find_packages

setup(
    name="cinema-toulouse",
    version="0.1",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        'flask',
        'flask-cors',
        'beautifulsoup4',
        'requests',
    ],
) 