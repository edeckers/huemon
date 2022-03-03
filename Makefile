# source: https://github.com/mozilla-services/telescope/pull/752/files

.PHONY: clean format help lint test

INSTALL_STAMP := .install.stamp
NAME := huemon

.DEFAULT_GOAL := help

help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo ""
	@echo "  clean       remove all temporary files"
	@echo "  format      reformat code"
	@echo "  install     install packages and prepare environment"
	@echo "  lint        run the code linters"
	@echo "  test        run all the tests"
	@echo ""
	@echo "Check the Makefile to know exactly what each target is doing."

clean:
	src/bin/clean.sh

format: $(INSTALL_STAMP)
	src/bin/format.sh

install: $(INSTALL_STAMP)
$(INSTALL_STAMP): pyproject.toml poetry.lock
	src/bin/install.sh

lint: $(INSTALL_STAMP)
	src/bin/lint.sh

test: $(INSTALL_STAMP)
	src/bin/test.sh
