from setuptools import setup

install_requires = [
    "Flask==3.0.0",
    "gunicorn==21.2.0",
    "pytz==2023.3.post1",
]


setup(
    install_requires=install_requires,
)