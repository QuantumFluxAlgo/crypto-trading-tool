from setuptools import setup, find_packages

setup(
    name="crypto_trading_tool",
    version="0.1.0",
    description="A crypto trading tool with automated migrations and tests",
    author="Your Name or Org",
    packages=find_packages(where="."),
    install_requires=[
        # pin or range your runtime deps here
        "SQLAlchemy>=1.4,<2.0",
        "alembic>=1.8,<2.0",
        # add other dependencies…
    ],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        # if you have console scripts:
        # "console_scripts": [
        #     "crypto-trade=app.cli:main",
        # ],
    },
)
