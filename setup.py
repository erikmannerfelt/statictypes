"""Setup statictypes."""
import setuptools

with open("README.md") as file:
    LONG_DESCRIPTION = file.read()


setuptools.setup(
    name="statictypes",
    version="0.0.1",
    author="Erik Schytt Holmlund",
    author_email="erik-holmlund@hotmail.com",
    description="Enforce type annotations",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/eriksholmlund/statictypes",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6"
)
