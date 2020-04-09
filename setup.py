"""setup."""
import setuptools

setuptools.setup(
    name="duckduckgo_images_api",
    version="0.1.2",
    url="https://github.com/deepanprabhu/duckduckgo-images-api",
    author="Deepan Prabhu Babu",
    description="DuckDuckGo Image Search Results - using Python !",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    keywords="duckduckgo image api",
    license="MIT",
    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=['requests>=2.18.4',],
    setup_requires=['pytest-runner', ],
    tests_require=['pytest', 'flake8>=3.3.0', 'tox>=2.7.0', 'vcrpy>=1.11.1'],
    extras_require={
        'packaging': ['setuptools>=38.6.0', 'twine>=1.11.0',],
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'License :: OSI Approved :: MIT License',
    ],
    #  entry_points={'console_scripts': []},
)
