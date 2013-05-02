from setuptools import setup, find_packages
import os

from events import get_version

README = os.path.join(os.path.dirname(__file__), 'README.rst')
long_description = open(README).read() + '\n\n'

setup(name='django-events-calendar',
      version=get_version().replace(' ', '-'),
      install_requires=['sorl-thumbnail==11.12', 'django-extensions'],
      author='Jacob Tuz Poot',
      author_email='jetp79@gmail.com',
      url='http://github.com/jtuz/django-events-calendar',
      description='Django app to manage and publish Events on a Web Site',
      long_description=long_description,
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      package_data={
             '': ['*.txt', '*.rst']
      },
      include_package_data=True,
      keywords='events django admin',
      license='BSD License',
      classifiers=['Development Status :: 3 - Alpha',
                   'Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'Natural Language :: Spanish',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python :: 2',
                   'License :: OSI Approved :: BSD License',
                   'Topic :: Internet',
                   'Topic :: Internet :: WWW/HTTP', ],
      zip_safe=False,
)
