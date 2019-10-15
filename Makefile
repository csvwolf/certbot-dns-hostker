test:
	python3 -m pylint certbot_dns_hostker
doc:
	pdoc --html --output-dir docs certbot_dns_hostker --force
compile:
	python3 setup.py sdist bdist_wheel
publish:
	make compile && python3 -m twine upload --skip-existing dist/*
.PHONY: test