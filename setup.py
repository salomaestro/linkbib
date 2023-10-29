from distutils.core import setup

setup(
    name="linkbib",
    version="0.1.0",
    packages=["linkbib"],
    author="Christian Salomonsen",
    maintainer="Christian Salomonsen",
    license="GNU GPLv3",
    install_requires=[
        "pyyaml",
        "sqlitedict",
    ],
    scripts=["bin/linkbib"],
)
