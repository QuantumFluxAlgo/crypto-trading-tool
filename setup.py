# setup.py
from setuptools import setup, find_packages

setup(
    name="crypto_trading_tool",
    version="0.1.0",
    packages=find_packages(where="."),
    install_requires=[
        # your runtime dependencies here, e.g. sqlalchemy, alembic
    ],
    include_package_data=True,
    zip_safe=False,
)
