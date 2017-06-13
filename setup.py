#!/usr/bin/env python
import os
from os.path import isdir, islink, relpath, dirname
import subprocess
import sys
from setuptools import (
    Command,
    setup,
    find_packages,
)

# Load constants.py without importing __init__.py, since pip
# calls setup.py before sqlalchemy is installed.
with open(os.path.join('src', 'sqlalchemy_rqlite', 'constants.py'), 'rt') as f:
    exec(f.read())


class PyTest(Command):
    user_options = [('match=', 'k', 'Run only tests that match the provided expressions')]

    def initialize_options(self):
        self.match = None

    def finalize_options(self):
        pass

    def run(self):
        testpath = 'src/test'
        buildlink = 'build/lib/test'

        if isdir(dirname(buildlink)):
            if islink(buildlink):
                os.unlink(buildlink)

            os.symlink(relpath(testpath, dirname(buildlink)), buildlink)
            testpath = buildlink

        try:
            os.environ['EPYTHON'] = 'python{}.{}'.format(sys.version_info.major, sys.version_info.minor)
            subprocess.check_call(['py.test', '-v', testpath,
                        '--cov-report=html', '--cov-report=term'] +
                       (['-k', self.match] if self.match else []) +
                       ['--cov={}'.format(p) for p in find_packages(dirname(testpath), exclude=['test'])])

        finally:
            if islink(buildlink):
                os.unlink(buildlink)


class PyLint(Command):
    user_options = [('errorsonly', 'E', 'Check only errors with pylint'),
                    ('format=', 'f', 'Change the output format')]

    def initialize_options(self):
        self.errorsonly = 0
        self.format = 'colorized'

    def finalize_options(self):
        pass

    def run(self):
        cli_options = ['-E'] if self.errorsonly else []
        cli_options.append('--output-format={0}'.format(self.format))
        errno = subprocess.call(['pylint'] + cli_options + [
            "--msg-template='{C}:{msg_id}:{path}:{line:3d},{column}: {obj}: {msg} ({symbol})'"] +
            find_packages('src', exclude=['test']), cwd='./src')
        raise SystemExit(errno)

setup_params = dict(
    name="sqlalchemy_rqlite",
    version=__version__,
    description="SQLAlchemy dialect for rqlite",
    author=__author__,
    author_email=__email__,
    maintainer=__author__,
    maintainer_email=__email__,
    install_requires=[
        "SQLAlchemy",
        "pyrqlite",
    ],
    dependency_links=['https://github.com/rqlite/pyrqlite/tarball/master#egg=pyrqlite-2'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Database :: Front-Ends',
    ],
    keywords='rqlite SQLAlchemy',
    package_dir={'': 'src'},
    packages=find_packages('src', exclude=['test']),
    include_package_data=True,
    platforms=['Posix'],
    cmdclass={'test': PyTest, 'lint': PyLint},
    entry_points={
        "sqlalchemy.dialects":
            ["rqlite.pyrqlite = sqlalchemy_rqlite.pyrqlite:dialect"]
    },
    license=__license__,
)

if __name__ == '__main__':
    setup(**setup_params)
