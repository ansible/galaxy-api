import setuptools


setuptools.setup(
    entry_points={
        'console_scripts': [
            'galaxy-api-manage=galaxy_api.manage:main',
        ]
    }
)
