from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# long description from README
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(name='roman_gen',
      version='0.1',
      description='Get your Julius Caesar on.',
      long_description=long_description,
      url='https://github.com/crricks/Python-Projects/tree/main/Roman%20Name%20Generator',
      packages=['roman_gen'])

