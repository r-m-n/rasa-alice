import io
import re

from setuptools import find_packages
from setuptools import setup


with io.open("README.rst", "rt", encoding="utf8") as f:
    readme = f.read()

with io.open("src/rasa_alice/__init__.py", "rt", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)


setup(
    name="rasa-alice",
    version=version,
    url="https://github.com/r-m-n/rasa-alice",
    license="MIT",
    description="Rasa Connector for Yandex Dialogs.",
    long_description=readme,
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=[
        "rasa>=1.5.0",
        "pydantic>=1.1.1"
    ],
    extras_require={
        "dev": [
            "pytest",
            "flake8",
            "tox"
        ]
    }
)
