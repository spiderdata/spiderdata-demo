from setuptools import setup, find_packages
setup(
    name="spiderdata-demo",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'Flask',
        'Flask-Cors',
        'Flask-HTTPAuth'
    ],
)
