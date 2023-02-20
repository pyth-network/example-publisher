from setuptools import setup, find_packages

setup(
    name="example-publisher",
    version="0.1.0",
    author="Pyth Data Association",
    author_email="",
    packages=find_packages(exclude=["tests"]),
    zip_safe=False,
    include_package_data=True,
    python_requires=">=3.9",
    install_requires=[
        "structlog",
        "click",
        "dataclasses_json",
        "structlog",
        "attr",
        "numpy",
        "jsonrpc_websocket",
        "pycoingecko>=2.2.0",
        "typed-settings>=0.11.1",
        "pythclient>=0.1.4",
    ],
    extras_require=dict(
        test=[
            "pylint",
            "pep8",
            "flake8",
            "pytest>=6.2.0",
        ],
        build=["setuptools-git", "wheel"],
    ),
)
