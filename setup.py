from setuptools import setup

setup(
    name='korean-name-generator',
    version='1.0.1',
    license='MIT',
    description='Generates random but reasonable Korean names',
    keywords='Korean',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Jinui You',
    author_email='baram991103@gmail.com',
    packages=['korean_name_generator'],
    install_requires=[],
    include_package_data=True,
    url='https://github.com/tinyjin/korean-name-generator',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)
