.PHONY: build init lint test

build: init
	src/bin/build.sh

init:
	src/bin/init.sh

lint:
	src/bin/lint.sh

test:
	src/bin/test.sh
