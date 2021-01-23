from setuptools import setup

# load readme
with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name="prettydraw",
    version="0.0.0",
    description="Draw pretty annotations using PIL.",
    py_modules=["prettydraw"],
    package_dir={'', "src"}
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "PIL",
        "numpy"
    ]
)