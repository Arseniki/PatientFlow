from setuptools import setup, find_packages

setup(
    name="PatientFlowSimulation",
    version="1.0.0",
    author="Groupe 10",
    author_email="abdoularsene@gmail.com",
    description="Discrete Event Simulation for M/M/c/k₀ Queuing Systems",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/simulation-des",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Langage de programmation :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=[
        "matplotlib>=3.5.0",
        "numpy>=1.21.0",
    ],
    entry_points={
        "console_scripts": [
            "simulation-des=main:main",
        ],
    },
)