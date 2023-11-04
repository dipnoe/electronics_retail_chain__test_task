docker-up:
	docker-compose up --build -d
docker-down:
	docker-compose down
docker-exec:
	docker-compose exec app bash