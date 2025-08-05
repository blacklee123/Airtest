clean:
	rm -rf dist
build: clean
	pip install setuptools wheel twine build
	python -m build

push: build
	twine upload -r coding-pypi dist/*