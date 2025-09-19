from setuptools import setup, find_packages

setup(
    name="coned-utility-scraper",
    version="0.2.0",
    packages=find_packages(),
    install_requires=[
        "pandas>=2.0",
        "python-dateutil>=2.8",
        "tqdm>=4.66",
        "selenium>=4.20",
        "PySide6>=6.7",
        "pillow>=10.0",
        "python-dotenv>=1.0",
    ],
    entry_points={"console_scripts": ["coned-ui=coned_utility.main:main"]},
)
