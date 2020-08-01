from setuptools import setup, find_packages
setup(
    name="Word_edit",
    version="0.1",
    packages=find_packages(),
    author="zhaofeng-shu33",
    description="backend for xinyu",
    url="https://github.com/zhaofeng-shu33/DeutschLernen_server",
    author_email="616545598@qq.com",
    install_requires=['lxml', 'beautifulsoup4'],
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Programming Language :: Python :: 3"
    ]
)
