.PHONY: clean-pyc clean-build docs clean

help:
	@echo "clean - remove all build, test, coverage and Python artifacts"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean-test - remove test and coverage artifacts"
	@echo "dist - package"
	@echo "install - install the package to the active Python's site-packages"

clean: clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	get . -name '*.egg-info' -exec rm -fr {} +
	get . -name '*.egg' -exec rm -f {} +

clean-pyc:
	get . -name '*.pyc' -exec rm -f {} +
	get . -name '*.pyo' -exec rm -f {} +
	get . -name '*~' -exec rm -f {} +
	get . -name '__pycache__' -exec rm -fr {} +

release: clean
	python setup.py sdist upload
	python setup.py bdist_wheel upload

dist: clean
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist
