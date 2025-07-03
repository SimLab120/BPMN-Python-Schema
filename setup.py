from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="bpmn-python-schema",
    version="1.0.0",
    author="SimLab120",
    author_email="simlab120@example.com",
    description="A comprehensive Python library for BPMN data modeling and validation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SimLab120/bpmn-python-schema",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Office/Business :: Scheduling",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "pre-commit>=3.0.0",
        ],
        "docs": [
            "sphinx>=6.0.0",
            "sphinx-rtd-theme>=1.2.0",
            "myst-parser>=1.0.0",
        ],
    },
    keywords="bpmn, business process, modeling, notation, workflow, process automation",
    project_urls={
        "Bug Reports": "https://github.com/SimLab120/bpmn-python-schema/issues",
        "Source": "https://github.com/SimLab120/bpmn-python-schema",
        "Documentation": "https://bpmn-python-schema.readthedocs.io/",
    },
)
