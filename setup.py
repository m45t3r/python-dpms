import setuptools

module = setuptools.Extension("dpms", libraries=["Xext",], sources=["./src/pydpms.c"])

with open("README.md", "r") as fh:
    long_description = fh.read()

if __name__ == "__main__":
    setuptools.setup(
        name="dpms",
        version="0.1.0",
        author="Thiago Kenji Okada",
        author_email="thiagokokada@gmail.com",
        description="Python Bindings to DPMS X11 extension",
        long_description=long_description,
        long_description_content_type="text/markdown",
        ext_modules=[module],
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Operating System :: POSIX",
        ],
        python_requires=">=3.5",
    )
