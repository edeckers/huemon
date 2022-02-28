#!/usr/bin/env python3

from distutils.core import setup

setup(
    author="Ely Deckers",
    author_email="noreply@nonono.com",
    description="Monitoring for Philips Hue",
    license="MPL-2.0",
    long_description=open("README").read(),
    name="huemon",
    packages=[
        "huemon",
        "huemon.api",
        "huemon.commands",
        "huemon.commands_available",
        "huemon.commands_internal",
        "huemon.discoveries",
        "huemon.discoveries_available",
        "huemon.infrastructure"],
    url="https://github.com/edeckers/huemon",
    version="0.0.2",
)
