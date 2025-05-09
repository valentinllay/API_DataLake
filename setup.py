from setuptools import setup, find_packages

setup(
 name="hello_world",
 version="0.1.0",
 packages=find_packages(where="src"),
 package_dir={"": "src"},
 install_requires=[
 # ajoute ici Flask si besoin, ex. "Flask>=2.2.5"
 ],
)