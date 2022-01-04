from setuptools import setup
import nicolive_dl

def _requires_from_file(filename):
    return open(filename).read().splitlines()

setup(
    name="nicolive_dl",
    version=nicolive_dl.__version__,
    license=nicolive_dl.__license__,
    description="ニコ生タイムシフトダウンローダー",
    author=nicolive_dl.__author__,
    author_email=nicolive_dl.__author_email__,
    url=nicolive_dl.__url__,
    packages=['nicolive_dl'],
    install_requires=_requires_from_file('requirements.txt'),
    entry_points={
        "console_scripts": ["nicolive_dl = nicolive_dl.__main__:main"]
    }
)
