"""
Setup of the VentoExpertSDK module
"""
from setuptools import setup

setup(
    name="VentoExpertSDK",
    version="0.1.0",
    description="Blauberg Vento Expert ventilation SDK",
    long_description=(
        "SDK for connection to the Blauberg Vento Expert and compatible producers ventilation. "
        "Made for interfacing to Home Assistant"
    ),
    author="Jens Østergaard Nielsen & Birger Kollstrand",
    url="https://github.com/BirgerKo/VentoExpertSDK",
    packages=["VentoExpertSDK"],
    license="GPL-3.0",
)
