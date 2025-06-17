u:
	docker compose up -d

d:
	docker compose down 

r:
	docker compose restart

b:
	docker compose up --build

mm:
	docker exec -it siteping-web-1 python manage.py makemigrations

m:
	docker exec -it siteping-web-1 python manage.py migrate

user:
	docker exec -it siteping-web-1 python manage.py createsuperuser
