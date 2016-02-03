from setuptools import setup
from setuptools.command.test import test as TestCommand
import sys


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)



setup(
    tests_require=['pytest'],
    cmdclass = { 'test' : PyTest },
    athor="@ScottHenning",
    author_email="shenning@cisco.com",
    description="A Python wrapper for Spark Developers API",
    install_requires=["requests"],
    keywords="spark api",
    license="MIT",
    name="pyCiscoSparkAPI",
    packages=["pyCiscoSparkAPI"],
    test_suite="tests",
    url="",
    version="0.0.1",
)
