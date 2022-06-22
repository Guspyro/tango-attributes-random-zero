from setuptools import setup, find_packages

# The version is updated automatically with bumpversion
# Do not update manually!!
__version__ = '0.1.0'


def main():

    setup(
        name='tangods-braggbugtest',
        version=__version__,
        package_dir={'tangods-braggbugtest': 'src'},
        packages=find_packages(),
        author="Miquel Navarro",
        author_email="mnavarro@cells.es",
        description="Test device to try to reproduce dmc_bragg bug",
        license='GPLv3+',
        url='https://git.cells.es/controls/tangods-ict',
        requires=['tango (>=8.1.0)'],
        entry_points={
            "console_scripts": ['BraggBugTest = src.braggbugtest:main'],
        },
    )


if __name__ == "__main__":
    main()
