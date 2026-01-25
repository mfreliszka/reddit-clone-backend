run:
	litestar run

lint:
	ruff check .
	ruff format --check .

format:
	ruff format .