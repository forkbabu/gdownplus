from __future__ import print_function

import distutils.spawn
import shlex
import subprocess
import sys

from setuptools import find_packages
from setuptools import setup

version = "3.12.2"


if sys.argv[1] == "release":
    if not distutils.spawn.find_executable("twine"):
        print(
            "Please install twine:\n\n\tpip install twine\n", file=sys.stderr
        )
        sys.exit(1)

    commands = [
        "git pull origin master",
        "git tag v{:s}".format(version),
        "git push origin master --tag",
        "python setup.py sdist",
        "twine upload dist/gdownplus-{:s}.tar.gz".format(version),
    ]
    for cmd in commands:
        subprocess.check_call(shlex.split(cmd))
    sys.exit(0)


def get_long_description():
    with open("README.md") as f:
        long_description = f.read()

    try:
        import github2pypi

        return github2pypi.replace_url(
            slug="wkentaro/gdownplus", content=long_description
        )
    except Exception:
        return long_description


setup(
    name="gdownplus",
    version=version,
    packages=find_packages(exclude=["github2pypi"]),
    install_requires=[
        "filelock",
        "requests[socks]",
        "six",
        "tqdm",
        "beautifulsoup4",
        "pathlib2",
        "future",
    ],
    description="gdownplus | gdown for big boys",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Sayantan Das",
    author_email="sdas.codes@gmail.com",
    url="http://github.com/forkbabu/gdownplus",
    license="MIT",
    keywords="Data Download",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    entry_points={"console_scripts": ["gdownplus=gdownplus.cli:main"]},
)
