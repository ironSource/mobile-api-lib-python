from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()
with open("requirements.txt", "r") as fh:
    requirements = [line.strip() for line in fh]
packages = [
    package for package in find_packages() if package.startswith("ironsource_api")
]
setup(
    name='ironsource-mobile-api',
    packages=packages,
    version='1.0.0',
    url='https://github.com/ironSource/mobile-api-lib-python',
    license='Apache-2.0',
    author='IronSource Ltd.',
    author_email='mobile-api-lib-ci@is.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=requirements,
    python_requires='>=3.7',
    
)
