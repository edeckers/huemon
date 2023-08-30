.PHONY: clean format help install lint release test

NAME := huemon

.DEFAULT_GOAL := help

help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo ""
	@echo "  clean       remove all temporary files"
	@echo "  format      reformat code"
	@echo "  install     install packages and prepare environment"
	@echo "  lint        run the code linters"
	@echo "  release     build a release and publish it"
	@echo "  test        run all the tests"
	@echo ""
	@echo "Check the Makefile to know exactly what each target is doing."

# PHONY
clean:
	src/bin/clean.sh

format: poetry.lock
	src/bin/format.sh

install: poetry.lock

lint: poetry.lock
	src/bin/lint.sh

release: poetry.lock
	assets/release/release-all.sh

test: poetry.lock
	src/bin/test.sh

# FILES
poetry.lock: .venv pyproject.toml
	touch poetry.lock

.venv: # assumption: .venv existst -> poetry is installed
	src/bin/install.sh
