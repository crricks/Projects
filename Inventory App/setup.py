from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# long description from README
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(name='inventory_app',
      version='0.1',
      description='Store and update items in inventory.',
      long_description=long_description,
      url='https://github.com/crricks/Python-Projects/tree/main/Inventory%20App',
      packages=find_packages(where='src'))
