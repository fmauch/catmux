#!/usr/bin/env python

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="catmux",
    version="0.3.4",
    license="MIT",
    author="Felix Exner",
    author_email="felix_mauch@web.de",
    description="A tmux orchestration package.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fmauch/catmux",
    packages=setuptools.find_packages(),
    scripts=["script/catmux_create_session"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["pyyaml"],
    python_requires=">=3.7",
    package_data={"catmux.resources": ["*.yaml", "*.txt", "*.conf"]},
)
