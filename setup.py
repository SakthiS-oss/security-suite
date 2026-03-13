from setuptools import setup, find_packages

setup(
    name="security-suite",  # Updated name
    version="4.0",
    author="Your Name",
    description="A professional multi-threaded password security suite",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/yourusername/security-suite",
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'security-suite=app:main', # You can now type this in terminal to launch
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)