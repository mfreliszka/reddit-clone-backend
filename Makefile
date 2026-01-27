run:
	litestar run

lint:
	ruff check .
	ruff format --check .

format:
	ruff format .

# Migrations
migration-new:
	uv run piccolo migrations new app --auto

migrate:
	uv run piccolo migrations forwards all

migrate-undo:
	uv run piccolo migrations backwards app 1

# Testing
test:
	uv run pytest tests/

test-snapshot:
	uv run pytest tests/ --snapshot-update

# Utilities
clean:
	find . -name "__pycache__" -type d -exec rm -rf {} +
	find . -name ".pytest_cache" -type d -exec rm -rf {} +
	find . -name ".ruff_cache" -type d -exec rm -rf {} +

# https://github.com/casey/just
# just is a command runner that is a simpler alternative to make.
