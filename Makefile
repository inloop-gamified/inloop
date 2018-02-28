IMAGE   := inloop-integration-test
TESTENV := PIPENV_DOTENV_LOCATION="$(shell pwd)/tests/.env"
SUITE   := tests

init:
	pipenv install --dev
	docker build -t $(IMAGE) tests/functional/testrunner
	ln -snf .env.develop .env

loaddb:
	pipenv run ./manage.py migrate
	pipenv run ./manage.py loaddata about_pages staff_group
	pipenv run ./manage.py loaddata demo_accounts development_site

test:
	env $(TESTENV) pipenv run ./manage.py test $(SUITE)

coverage:
	env $(TESTENV) pipenv run coverage run ./manage.py test $(SUITE)
	pipenv run coverage report

lint:
	pipenv run isort --quiet --check-only
	pipenv run flake8

.PHONY: init loaddb test coverage lint
