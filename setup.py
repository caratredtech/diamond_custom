from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in diamond_customapp/__init__.py
from diamond_customapp import __version__ as version

setup(
	name="diamond_customapp",
	version=version,
	description="custom app for diamond",
	author="kiran@caratred.com",
	author_email="kiran@caratred.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
