.PHONY: build init

build:
	src/bin/build.sh

init:
	cd src && pip3 install -r requirements.txt

