from setuptools import setup, find_packages

setup(
    name="logger",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'grpcio-tools',
    ],
    author="Retendo Contributors",
    description="Logger for Python NEX Server.", 
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
