import os

from setuptools import setup

classifiers = [
    'Programming Language :: Python :: 3',
]

name = 'at_tracker'
description = 'AT Tracker'
version = '0.1'
author = 'dpooley'
author_email = 'daniel.pooley@gmail.com'
url = 'http://at.dan.org.nz'

requirements = [l.strip() for l in open('requirements.txt').readlines()]
scripts = [f.strip('.py') for f in os.listdir('scripts')]
packages = [name] + [f'{name}.{d}' for d in next(os.walk('.'))[1]]
package_dir = {name: ''}
for p in packages:
    package_dir[f'{name}.{p}'] = p

print(package_dir, packages)

setup(name=name,
      version=version,
      description=description,
      author=author,
      author_email=author_email,
      url=url,
      package_dir=package_dir,
      packages=packages,
      install_requires=requirements,
      include_package_data=True,
      classifiers=classifiers,
      test_suite='tests',
      entry_points = {
        'console_scripts': [
            [f'{script}={name}.scripts.{script}:main'] for script in scripts
        ]
      })
