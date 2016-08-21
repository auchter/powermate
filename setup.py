from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='powermate',
    version='0.0.2',
    description='Library for Griffin Powermate Bluetooth controllers',
	long_description=long_description,
    url='https://github.com/auchter/powermate',
    author='Michael Auchter',
    author_email='a@phire.org',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='powermate bluetooth',
    packages=['powermate'],
    install_requires=['bluepy'],
    entry_points={
        'console_scripts': [
            'powermate-demo=powermate.demo:main'
        ]
    }
)
