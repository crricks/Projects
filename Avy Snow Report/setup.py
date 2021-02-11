from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# long description from README
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(name='avyReport',
      version='0.1',
      description='Scrape North San Juan avalanche data',
      long_description=long_description,
      url='https://github.com/crricks/Python-Projects/tree/main/Avy%20Snow%20Report',
      packages=['avyReport'])
