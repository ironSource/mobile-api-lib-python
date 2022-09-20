from setuptools import setup, find_packages
import versioneer

with open("README.md", "r") as fh:
    long_description = fh.read()
with open("requirements.txt", "r") as fh:
    requirements = [line.strip() for line in fh]

setup(
    name='ironsource_api',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    package_dir={'':'ironsource_api'},
    packages=find_packages("ironsource_api",exclude=['tests']),
    url='https://github.com/ironSource/mobile-api-lib-python',
    license='MIT',
    author='IronSource Mobile',
    author_email='mobile-api-lib-ci@is.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=requirements,
    python_requires='>=3.7',
    
)
