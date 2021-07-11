from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

with open("requirements.txt") as f:
    requirements = [r.strip() for r in f.readlines()]

print(requirements)
name = 'image-dl'
setup(
    name=name,
    packages=find_packages(),
    version='0.0.2',
    license='MIT',
    description='A fast and simple image downloader in python',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f'https://github.com/sdtblck/{name}',
    author='Sid Black',
    author_email='sdtblck@gmail.com',
    install_requires=[],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10'
    ],
)
