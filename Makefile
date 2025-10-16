.PHONY: start stop restart build logs shell test test-unit test-integration test-docker clean-test clean dev-setup lint linter lint-fix-long-lines mypy check

# 🚀 Development Commands

# Start the development environment
start:
	@./scripts/dev-start.sh

# Stop all services
stop:
	@echo "🛑 Stopping services..."
	docker-compose down

# Restart services
restart: stop start

# Build services
build:
	@echo "🔨 Building services..."
	docker-compose build

# View logs
logs:
	@echo "📋 Viewing logs..."
	docker-compose logs -f

# Access backend shell
shell:
	@echo "🐚 Accessing backend shell..."
	docker-compose exec web bash

# Access database shell
db-shell:
	@echo "🗄️  Accessing database shell..."
	docker-compose exec db psql -U postgres -d airesume_dev

# View database logs
db-logs:
	@echo "📋 Viewing database logs..."
	docker-compose logs -f db

# Reset database (WARNING: This will delete all data!)
db-reset:
	@echo "⚠️  Resetting database (this will delete all data)..."
	@read -p "Are you sure? Type 'yes' to continue: " confirm && [ "$$confirm" = "yes" ] || exit 1
	docker-compose stop web
	docker-compose exec db psql -U postgres -c "DROP DATABASE IF EXISTS airesume_dev;"
	docker-compose exec db psql -U postgres -c "CREATE DATABASE airesume_dev;"
	docker-compose start web
	@echo "✅ Database reset complete!"

# Fix PostgreSQL version incompatibility
db-fix-version:
	@echo "🔧 Fixing PostgreSQL version incompatibility..."
	@echo "This will delete all database data and recreate with the correct version."
	@read -p "Continue? Type 'yes': " confirm && [ "$$confirm" = "yes" ] || exit 1
	docker-compose down
	docker volume rm $$(docker volume ls -q | grep db_data) 2>/dev/null || true
	@echo "✅ Database volume removed. Run 'make start' to recreate with correct version."

# Run database migrations
migrate:
	@echo "🔄 Running database migrations..."
	docker-compose exec web alembic upgrade head

# Create new migration
migration:
	@echo "📝 Creating new migration..."
	@read -p "Enter migration message: " message; \
	docker-compose exec web alembic revision --autogenerate -m "$$message"

# Install new Python package
install:
	@echo "📦 Installing Python package..."
	@read -p "Enter package name: " package; \
	docker-compose exec web uv add "$$package"
	docker-compose restart web

# Setup development environment
dev-setup:
	@echo "🛠️  Setting up development environment..."
	@if [ ! -f .env ]; then \
		echo "📝 Creating .env file from template..."; \
		cp .env.example .env; \
		echo "⚠️  Please update .env with your configuration"; \
	fi
	@echo "🔨 Building containers..."
	docker-compose build
	@echo "🗄️  Setting up database..."
	docker-compose up -d db
	@echo "⏳ Waiting for database to be ready..."
	@sleep 10
	@echo "✅ Development environment ready!"
	@echo "Run 'make start' to start all services"

# Clean development environment
clean:
	@echo "🧹 Cleaning development environment..."
	docker-compose down -v
	docker system prune -f
	@echo "✅ Environment cleaned!"

# 🧪 Testing Commands

# Ejecutar todas las pruebas con Docker
test:
	@echo "🧪 Ejecutando todas las pruebas con Docker..."
	./scripts/run-tests.sh

# Ejecutar solo pruebas unitarias
test-unit:
	@echo "🧪 Ejecutando pruebas unitarias..."
	docker-compose -f docker-compose.test.yml run --rm unit-tests

# Ejecutar solo pruebas de integración
test-integration:
	@echo "🧪 Ejecutando pruebas de integración..."
	docker-compose -f docker-compose.test.yml run --rm integration-tests

# Ejecutar pruebas con Docker (sin script)
test-docker:
	@echo "🧪 Ejecutando pruebas con Docker..."
	docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit
	docker-compose -f docker-compose.test.yml down -v

# Limpiar contenedores y volúmenes de prueba
clean-test:
	@echo "🧹 Limpiando contenedores y volúmenes de prueba..."
	docker-compose -f docker-compose.test.yml down -v
	docker system prune -f

# Ejecutar pruebas específicas
test-subscription:
	@echo "🧪 Ejecutando pruebas de suscripción..."
	docker-compose -f docker-compose.test.yml run --rm unit-tests pytest tests/unit/user/test_subscription* tests/integration/test_subscription* -v

# Ejecutar pruebas de interview templates
test-interview-templates:
	@echo "🧪 Ejecutando pruebas de interview templates..."
	docker-compose -f docker-compose.test.yml run --rm integration-tests pytest tests/integration/test_interview_templates.py -v

# Ejecutar pruebas de integración sin las marcadas como skip
test-integration-quick:
	@echo "🧪 Ejecutando pruebas de integración rápidas..."
	docker-compose -f docker-compose.test.yml run --rm integration-tests pytest tests/integration/ -m "not skip" -v

# Ejecutar pruebas con cobertura
test-coverage:
	@echo "🧪 Ejecutando pruebas con cobertura..."
	docker-compose -f docker-compose.test.yml run --rm unit-tests pytest --cov=src --cov-report=html --cov-report=term-missing

# 🔍 Code Quality Commands

# Ejecutar mypy type checking
mypy:
	@echo "🔍 Ejecutando verificación de tipos con mypy..."
	docker-compose exec web mypy src/ presentation/

# Ejecutar flake8 linting y corregir W291, W292, W293, E302
lint:
	@echo "🔍 Ejecutando linting con flake8..."
	docker-compose exec web uv run flake8 src/ presentation/
	@echo "🔧 Corrigiendo errores W291, W292, W293, E302..."
	docker-compose exec web uv run autopep8 --select=W291,W292,W293,E302 --in-place --recursive src/ presentation/

# Ejecutar linting con flake8
linter:
	@echo "🔍 Ejecutando linting con flake8..."
	docker-compose exec web uv run flake8 src/ presentation/

# Corregir errores E501 (line too long) con autopep8 agresivo
lint-fix-long-lines:
	@echo "🔧 Corrigiendo errores E501 (line too long) con modo agresivo..."
	docker-compose exec web uv run autopep8 --select=E501 --aggressive --in-place --recursive src/ presentation/
	@echo "✅ Líneas largas corregidas!"

# Ejecutar verificación completa de calidad del código
check:
	@echo "🔍 Ejecutando verificación completa de calidad del código..."
	@echo "📋 Ejecutando flake8..."
	docker-compose exec web uv run flake8 src/ presentation/
	@echo "📋 Ejecutando mypy..."
	docker-compose exec web mypy src/ presentation/
	@echo "✅ Verificación completa!"

# Ayuda
help:
	@echo "Comandos disponibles:"
	@echo "🧪 Testing:"
	@echo "  make test              - Ejecutar todas las pruebas con Docker"
	@echo "  make test-unit         - Ejecutar solo pruebas unitarias"
	@echo "  make test-integration  - Ejecutar solo pruebas de integración"
	@echo "  make test-docker       - Ejecutar pruebas con Docker (directo)"
	@echo "  make test-subscription - Ejecutar pruebas de suscripción"
	@echo "  make test-coverage     - Ejecutar pruebas con cobertura"
	@echo "🔍 Code Quality:"
	@echo "  make lint              - Ejecutar linting con flake8 y corregir W291, W292, W293, E302"
	@echo "  make linter            - Ejecutar linting con flake8 (solo verificar)"
	@echo "  make lint-fix-long-lines - Corregir errores E501 (líneas largas) con modo agresivo"
	@echo "  make mypy              - Ejecutar verificación de tipos con mypy"
	@echo "  make check             - Verificación completa (flake8 + mypy)"
	@echo "🛠️ Utilities:"
	@echo "  make clean-test        - Limpiar contenedores y volúmenes"
	@echo "  make help              - Mostrar esta ayuda"