from setuptools import setup, find_packages

setup(
    name='cs4098-analytics',
    version='1.0',
    description='Web scraping API for zbMATH records info (including software)',
    author='Orion Portelli',
    author_email='jeffersonorionportelli@gmail.com',
    packages=find_packages(),
    install_requires=['beautifulsoup4', 'lxml', 'requests', 'Flask', 'Flask-RESTful', 'pandas', 'matplotlib']
)