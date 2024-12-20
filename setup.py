from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="carboncalc",  # Nom du package
    version="0.1.0",
    author="Issa KA",
    author_email="kai658366@gmail.com",
    description="Outil pour calculer les émissions de carbone",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=open("requirements.txt").read().splitlines(),
    entry_points={
        'console_scripts': [
            'carboncalc=carboncalc.main:main',
        ],
    },
)
