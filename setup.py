import os
from distutils.core import setup

docs = [os.path.join('docs', x) for x in os.listdir('docs')]
examples = docs = [os.path.join('examples', x) for x in os.listdir('examples')]

setup(name="CLI",
        version="0.1",
        description="Simple, Object-Oriented approach to Python CLI apps",
        author="Will Maier",
        author_email="will@m.aier.us",
        url="http://code.lfod.us/cli",
        data_files=[
            ('share/doc/py-cli/', docs),
            ('share/examples/py-cli/', examples)],
        py_modules=['cli'])