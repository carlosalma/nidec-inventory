from setuptools import setup, find_packages

setup(
    name="nidec-inventory",
    version="v0.0b1",
    description="Nidec Unidrive M motor control drives inventory generator.",
    long_description=open('README.md',"r", encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    author="Carlos Alonso Martín",
    author_email="cam.codeweaver@gmail.com",
    url="https://github.com/carlosalma/nidec-inventory",
    project_urls={"Github": "github.com/carlosalma/nidec-inventory",},
    license="MIT License",
    packages=find_packages(),
    package_data={'': ["*.yaml"]}
)
