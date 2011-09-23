from setuptools import setup, find_packages
import os

version = '1.0b7'

setup(name='collective.gallery',
      version=version,
      description="Base gallery product for plone with picasa and flickr support by Makina Corpus",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='JeanMichel FRANCOIS aka toutpt',
      author_email='jeanmichel.francois@makina-corpus.com',
      url='https://svn.plone.org/svn/collective/collective.gallery',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'gdata',
          'flickrapi',
          'collective.js.galleriffic',
          # -*- Extra requirements: -*-
      ],
      extras_require = dict(
          tests=['plone.app.testing'],
          facebook=[], #was beautifulsoup
      ),
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
