#!/usr/bin/env python3

from distutils.core import setup

setup(
  author="Ely Deckers",
  author_email="noreply@nonono.com",
  description="Monitoring for Philips Hue",
  long_description=open("README").read(),
  name="huemon",
  packages=["huemon", "huemon.api", "commands_available", "discoveries_available"],
  url="https://deckers.io",
  version="0.0.1",
)
