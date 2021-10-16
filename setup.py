import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DoraPy",
    version="1.0.0",
    author="pgCai",
    author_email="pgcai@tju.edu.cn",
    description="Dorapy is a deep learning framework that focuses on data preprocessing.🛸",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CPG123456/DoraPy",
    project_urls={
        "Bug Tracker": "https://github.com/CPG123456/DoraPy/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)