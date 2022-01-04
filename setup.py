from setuptools import setup
from nicolive_dl import __version__

def _requires_from_file(filename):
    return open(filename).read().splitlines()

setup(
    name="nicolive_dl",
    version=__version__,
    license="MIT",
    description="ニコ生タイムシフトダウンローダー",
    author="kairi",
    url="https://github.com/kairi003/nicolive-dl",
    packages=['nicolive_dl'],
    install_requires=_requires_from_file('requirements.txt'),
    entry_points={
        "console_scripts": ["nicolive_dl = nicolive_dl.__main__:main"]
    }
)
