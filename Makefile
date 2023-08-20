
migrate:
	alembic revision --autogenerate -m "Creating"
	alembic upgrade head