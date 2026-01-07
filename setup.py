from setuptools import setup, find_packages

setup(
    name="scribe",
    version="0.1.0",
    description="Turn your git commits into tweets",
    author="Quaternion Studios",
    packages=find_packages(),
    install_requires=[
        "openai>=1.0.0",
        "python-dotenv>=1.0.0",
        "gitpython>=3.1.0",
    ],
    entry_points={
        "console_scripts": [
            "scribe=scribe.cli:main",
        ],
    },
    python_requires=">=3.8",
)
