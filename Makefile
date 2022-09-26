run:
	python3 -W ignore manage.py runserver 127.0.0.1:8000

makemigrations:
	python3 -W ignore manage.py makemigrations

migrate:
	python3 -W ignore manage.py migrate
superuser:
	python3 -W ignore manage.py createsuperuser
newapp:
	python3 -W ignore manage.py startapp newapp