"""setup."""
import setuptools

setuptools.setup(
    name="duckduckgo_images_api",
    version="0.1.0",
    url="https://github.com/rachmadaniHaryono/google-images-download",

    author="Deepan Prabhu Babu",

    description="Using python to scrape DuckDuckGo Image Search Resuts",
    long_description=open('README.rst').read(),
    keywords="duckduckgo image downloader",
    license="MIT",

    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=True,

    install_requires=[
        'click>=6.7',
        'requests>=2.18.4',
        'structlog>=17.2.0',
    ],
    setup_requires=['pytest-runner', ],
    tests_require=['pytest', ],
    extras_require={
        'server': [
            'Flask-Admin>=1.5.0',
            'Flask-Bootstrap>=3.3.7.1',
            'Flask-SQLAlchemy>=2.3.1',
            'Flask-WTF>=0.14.2',
            'Flask>=0.12.2',
            'SQLAlchemy-Utils>=0.32.18',
        ],
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'License :: OSI Approved :: MIT License',
    ],

    entry_points={
        'console_scripts': [
            'duckduckgo-images-api = google_images_download.__main__:cli',
        ]
    },
)
