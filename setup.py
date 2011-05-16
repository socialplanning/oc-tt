from setuptools import setup, find_packages

version = '0.1.2'

setup(name='oc-tt',
      version=version,
      description="opencore tasktracker client package",
      long_description="""\
""",
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Framework :: Zope3",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='The Open Planning Project',
      author_email='',
      url='',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['opencore'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'oc-cab'
      ],
      entry_points="""
      # -*- Entry points: -*-
      [opencore.versions]
      oc-tt = opencore.tasktracker
      [topp.zcmlloader]
      opencore = opencore.tasktracker
      """,
      )
