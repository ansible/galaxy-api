import setuptools


setuptools.setup(
    entry_points={
        'console_scripts': ['galaxy-manage = galaxy_api.manage:main'],
    },
)
