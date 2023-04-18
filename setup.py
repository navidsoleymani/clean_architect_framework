from setuptools import setup, find_packages

setup(
    name='pyelzhen',
    version='0.0.999991',
    license='ELZHEN',
    author='elzhen_developers',
    author_email='support@elzhen.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='http://192.168.59.2/elzhendevelopers/pyelzhen.git',
    keywords='',
    install_requires=[
        'pydantic',
        'Django',
        'djangorestframework',
        'markdown',
        'django-filter',
    ],
)
