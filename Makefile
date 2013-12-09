APP=cexbot
DATE=$(shell date +%I:%M%p)

publish:
	./bin/write_version
	VERSION=$(shell cat VERSION)
	git add VERSION
	@git ci -m "${VERSION}"
	git tag ${VERSION}
	git push origin --all
	git push bb --all
	python setup.py publish

clean:
	find . -name *.pyc -exec rm -f {} \;