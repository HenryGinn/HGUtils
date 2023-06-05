from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = "1.0"
DESCRIPTION = "A triple of tools used for plotting, handling key-words, and utilities"
LONG_DESCRIPTION = ("Defaults: manages settings for classes that can be controlled easily from an interface.\n"
                    "Plotting: a front end for matplotlib to easily create subplots.\n"
                    "Utils: a collection of generally useful functions")

# Setting up
setup(
    name="hgutils",
    version=VERSION,
    author="Henry Ginn",
    author_email="<henryginn137@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=["matplotlib", "numpy", "screeninfo", "PIL"],
    keywords=["python", "matplotlib", "plotting", "default", "keywords", "utils"],
    classifiers=[
        "Development Status :: 1 - Alpha Testing",
        "Intended Audience :: Personal use + morons",
        "Programming Language :: Python :: 3",
        "Operating System :: Ubuntu",
        "Operating System :: Microsoft :: Windows",
    ]
)