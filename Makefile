help:
	@echo "Use 'make <ROOT>' where <ROOT> is one of"
	@echo "  venv:                 to create virtualenv and install dependencies"
	@echo "  dependencies:         to install project dependencies"
	@echo "  run-dev-server:       to run development server"
	@echo "  migrate:              to make migrations and migrate database"
	@echo "  test:                 to run django tests"


venv:
	virtualenv venv
	source venv/bin/activate
	pip install -r requirements.txt


dependencies:
	pip install -r requirements.txt


run-dev-server:
	export DJANGO_SETTINGS_MODULE=course_scheduler.settings.development
	python manage.py runserver


migrate:
	python manage.py makemigrations
	python manage.py migrate


test:
	python manage.py test
