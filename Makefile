help:
	@echo "Use 'make <ROOT>' where <ROOT> is one of"
	@echo "  venv:                 to create virtualenv and install dependencies"
	@echo "  dependencies:         to install project dependencies"
	@echo "  run-dev-server:       to run development server"
	@echo "  migrate:              to make migrations and migrate database"
	@echo "  test:                 to run django tests"
	@echo "  run-docker-compose:   to docker-compose up and serve static files"
	@echo "  gen-fake-data:        to generate some testing data for docker-compose"


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
	export DJANGO_SETTINGS_MODULE=course_scheduler.settings.development
	python manage.py makemigrations
	python manage.py migrate


test:
	python manage.py test


run-docker-compose:
	docker-compose up -d --build
	docker-compose exec backend python manage.py collectstatic --noinput
	docker-compose exec backend python manage.py migrate

gen-fake-data:
	docker-compose exec backend python manage.py flush_db
	docker-compose exec backend python manage.py generate_fake_data

