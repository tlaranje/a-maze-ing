from setuptools import setup, find_packages

setup(
    name="mazegen",
    version="1.0.0",
    author="Tiago Pinho & Joel Souza",
    author_email="tiagopinho4023@gmail.com & joelsantossouza08@gmail.com",
    description="A reusable MazeGenerator module for generating mazes.",
    long_description=open("README.md", encoding="utf-8").read()
    if "README.md" else "",
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.10",
)
