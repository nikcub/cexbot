PREFIX=/usr/local
APP=cexbot
DATE=$(shell date +%I:%M%p)
PYTHON=$(shell which python)

publish:
	./bin/write_version
	VERSION=$(shell cat VERSION)
	git add VERSION
	@git ci -m "`cat VERSION`"
	git tag `cat VERSION`
	git push origin --all
	git push bb --all
	python setup.py publish

clean:
	$(PYTHON) setup.py clean --all
	find . -name *.pyc -exec rm -f {} \;
	rm -rf build/*
	rm -rf dist/*
