from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pyhobo",  # Replace with your own username
    version="0.0.1",
    author="Himanshu Sahu",
    author_email="himanshu.sahu@uwaterloo.ca",
    description="PyHOBO allows to construct Hamiltonian for Variation Quantum Algorithms based on Higher-Order Binary Optimization.",
    long_description= "If you want to solve a combinatorial optimization problem using Higher-Order Binary Optimization, PyHOBO allows you to construct cost function or Hamiltonian for your problem which can directly be fed to Qiskit.",
    long_description_content_type="text/markdown",
    url="https://github.com/Manolin-git/pyhobo",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
