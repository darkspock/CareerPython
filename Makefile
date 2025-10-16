.PHONY: start stop restart build logs shell test test-unit test-integration test-docker clean-test clean dev-setup lint linter lint-fix-long-lines mypy check

# 🚀 Development Commands

# Start the development environment
start:
	@echo "🚀 Starting development environment..."
	@echo "📦 Starting Docker services..."
	docker-compose up -d
	@echo "🐍 Starting FastAPI server locally..."
	source .venv/bin/activate && uvicorn main:app --host 0.0.0.0 --port 8000 --reload

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

# Activate local Python environment
shell:
	@echo "🐚 Activating local Python environment..."
	source .venv/bin/activate && bash

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
	source .venv/bin/activate && alembic upgrade head

# Create new migration
migration:
	@echo "📝 Creating new migration..."
	@read -p "Enter migration message: " message; \
	source .venv/bin/activate && alembic revision --autogenerate -m "$$message"

# Install new Python package
install:
	@echo "📦 Installing Python package..."
	@read -p "Enter package name: " package; \
	source .venv/bin/activate && uv add "$$package"

# Setup development environment
dev-setup:
	@echo "🛠️  Setting up development environment..."
	@if [ ! -f .env ]; then \
		echo "📝 Creating .env file from template..."; \
		cp .env.example .env; \
		echo "⚠️  Please update .env with your configuration"; \
	fi
	@echo "🐍 Creating local virtual environment..."
	uv venv .venv --clear
	@echo "📦 Installing dependencies..."
	source .venv/bin/activate && uv pip install -e .
	@echo "🗄️  Starting database services..."
	docker-compose up -d
	@echo "⏳ Waiting for database to be ready..."
	@sleep 10
	@echo "✅ Development environment ready!"
	@echo "Run 'make start' to start the development server"

# Clean development environment
clean:
	@echo "🧹 Cleaning development environment..."
	docker-compose down -v
	docker system prune -f
	@echo "✅ Environment cleaned!"

# 🧪 Testing Commands

# Ejecutar todas las pruebas localmente
test:
	@echo "🧪 Ejecutando todas las pruebas localmente..."
	source .venv/bin/activate && pytest tests/ -v

# Ejecutar solo pruebas unitarias
test-unit:
	@echo "🧪 Ejecutando pruebas unitarias..."
	source .venv/bin/activate && pytest tests/unit/ -v

# Ejecutar solo pruebas de integración (requiere Docker para servicios)
test-integration:
	@echo "🧪 Ejecutando pruebas de integración..."
	@echo "🐳 Iniciando servicios de prueba..."
	docker-compose -f docker-compose.test.yml up -d test-db test-redis
	@echo "⏳ Esperando a que los servicios estén listos..."
	@sleep 10
	source .venv/bin/activate && POSTGRES_HOST=localhost POSTGRES_PORT=5434 REDIS_HOST=localhost REDIS_PORT=6380 TEST_DATABASE_URL="postgresql://test_user:test_password@localhost:5434/test_career_db" pytest tests/integration/ -v
	@echo "🧹 Deteniendo servicios de prueba..."
	docker-compose -f docker-compose.test.yml down

# Limpiar contenedores y volúmenes de prueba
clean-test:
	@echo "🧹 Limpiando contenedores y volúmenes de prueba..."
	docker-compose -f docker-compose.test.yml down -v
	docker system prune -f

# Ejecutar pruebas específicas
test-subscription:
	@echo "🧪 Ejecutando pruebas de suscripción..."
	source .venv/bin/activate && pytest tests/unit/user/test_subscription* tests/integration/test_subscription* -v

# Ejecutar pruebas de interview templates
test-interview-templates:
	@echo "🧪 Ejecutando pruebas de interview templates..."
	@echo "🐳 Iniciando servicios de prueba..."
	docker-compose -f docker-compose.test.yml up -d test-db test-redis
	@sleep 10
	source .venv/bin/activate && POSTGRES_HOST=localhost POSTGRES_PORT=5434 pytest tests/integration/test_interview_templates.py -v
	docker-compose -f docker-compose.test.yml down

# Ejecutar pruebas de integración sin las marcadas como skip
test-integration-quick:
	@echo "🧪 Ejecutando pruebas de integración rápidas..."
	@echo "🐳 Iniciando servicios de prueba..."
	docker-compose -f docker-compose.test.yml up -d test-db test-redis
	@sleep 10
	source .venv/bin/activate && POSTGRES_HOST=localhost POSTGRES_PORT=5434 pytest tests/integration/ -m "not skip" -v
	docker-compose -f docker-compose.test.yml down

# Ejecutar pruebas con cobertura
test-coverage:
	@echo "🧪 Ejecutando pruebas con cobertura..."
	source .venv/bin/activate && pytest tests/ --cov=src --cov-report=html --cov-report=term-missing -v

# 👥 Candidate Domain Tests

# Ejecutar todas las pruebas del dominio candidate
test-candidate:
	@echo "👥 Ejecutando todas las pruebas del dominio candidate..."
	source .venv/bin/activate && pytest tests/unit/candidate/ -v

# Ejecutar pruebas de comandos del dominio candidate
test-candidate-commands:
	@echo "⚡ Ejecutando pruebas de comandos candidate..."
	source .venv/bin/activate && pytest tests/unit/candidate/commands/ -v

# Ejecutar pruebas de queries del dominio candidate
test-candidate-queries:
	@echo "🔍 Ejecutando pruebas de queries candidate..."
	source .venv/bin/activate && pytest tests/unit/candidate/queries/ -v

# Ejecutar pruebas específicas de candidate (create, update)
test-candidate-crud:
	@echo "📝 Ejecutando pruebas CRUD de candidate..."
	source .venv/bin/activate && pytest tests/unit/candidate/commands/test_candidate_commands.py -v

# Ejecutar pruebas específicas de experience (create, update)
test-candidate-experience:
	@echo "💼 Ejecutando pruebas de experience..."
	source .venv/bin/activate && pytest tests/unit/candidate/commands/test_experience_commands.py -v

# Ejecutar pruebas específicas de education (create, update)
test-candidate-education:
	@echo "🎓 Ejecutando pruebas de education..."
	source .venv/bin/activate && pytest tests/unit/candidate/commands/test_education_commands.py -v

# Ejecutar pruebas específicas de project (create, update)
test-candidate-projects:
	@echo "🚀 Ejecutando pruebas de projects..."
	source .venv/bin/activate && pytest tests/unit/candidate/commands/test_project_commands.py -v

# Ejecutar pruebas del dominio candidate con cobertura
test-candidate-coverage:
	@echo "📊 Ejecutando pruebas candidate con cobertura..."
	source .venv/bin/activate && pytest tests/unit/candidate/ --cov=src/candidate/application --cov-report=html --cov-report=term-missing -v

# Ejecutar pruebas candidate con output verbose y colores
test-candidate-verbose:
	@echo "📝 Ejecutando pruebas candidate con output detallado..."
	source .venv/bin/activate && pytest tests/unit/candidate/ -v -s --tb=short --color=yes

# 🔍 Code Quality Commands

# Ejecutar mypy type checking
mypy:
	@echo "🔍 Ejecutando verificación de tipos con mypy..."
	source .venv/bin/activate && mypy src/ adapters/

# Ejecutar flake8 linting y corregir W291, W292, W293, E302
lint:
	@echo "🔍 Ejecutando linting con flake8..."
	source .venv/bin/activate && flake8 src/ adapters/
	@echo "🔧 Corrigiendo errores W291, W292, W293, E302..."
	source .venv/bin/activate && autopep8 --select=W291,W292,W293,E302 --in-place --recursive src/ adapters/

# Ejecutar linting con flake8
linter:
	@echo "🔍 Ejecutando linting con flake8..."
	source .venv/bin/activate && flake8 src/ adapters/

# Corregir errores E501 (line too long) con autopep8 agresivo
lint-fix-long-lines:
	@echo "🔧 Corrigiendo errores E501 (line too long) con modo agresivo..."
	source .venv/bin/activate && autopep8 --select=E501 --aggressive --in-place --recursive src/ adapters/
	@echo "✅ Líneas largas corregidas!"

# Ejecutar verificación completa de calidad del código
check:
	@echo "🔍 Ejecutando verificación completa de calidad del código..."
	@echo "📋 Ejecutando flake8..."
	source .venv/bin/activate && flake8 src/ adapters/
	@echo "📋 Ejecutando mypy..."
	source .venv/bin/activate && mypy src/ adapters/
	@echo "✅ Verificación completa!"

# Ayuda
help:
	@echo "Comandos disponibles:"
	@echo "🧪 Testing:"
	@echo "  make test              - Ejecutar todas las pruebas localmente"
	@echo "  make test-unit         - Ejecutar solo pruebas unitarias"
	@echo "  make test-integration  - Ejecutar solo pruebas de integración (con Docker para servicios)"
	@echo "  make test-subscription - Ejecutar pruebas de suscripción"
	@echo "  make test-coverage     - Ejecutar pruebas con cobertura"
	@echo "👥 Candidate Domain Tests:"
	@echo "  make test-candidate           - Ejecutar todas las pruebas del dominio candidate"
	@echo "  make test-candidate-commands  - Ejecutar pruebas de comandos candidate"
	@echo "  make test-candidate-queries   - Ejecutar pruebas de queries candidate"
	@echo "  make test-candidate-crud      - Ejecutar pruebas CRUD de candidate"
	@echo "  make test-candidate-experience - Ejecutar pruebas de experience"
	@echo "  make test-candidate-education - Ejecutar pruebas de education"
	@echo "  make test-candidate-projects  - Ejecutar pruebas de projects"
	@echo "  make test-candidate-coverage  - Ejecutar pruebas candidate con cobertura"
	@echo "  make test-candidate-verbose   - Ejecutar pruebas candidate con output detallado"
	@echo "🔍 Code Quality:"
	@echo "  make lint              - Ejecutar linting con flake8 y corregir W291, W292, W293, E302"
	@echo "  make linter            - Ejecutar linting con flake8 (solo verificar)"
	@echo "  make lint-fix-long-lines - Corregir errores E501 (líneas largas) con modo agresivo"
	@echo "  make mypy              - Ejecutar verificación de tipos con mypy"
	@echo "  make check             - Verificación completa (flake8 + mypy)"
	@echo "🛠️ Utilities:"
	@echo "  make clean-test        - Limpiar contenedores y volúmenes de prueba"
	@echo "  make shell             - Activar entorno Python local"
	@echo "  make help              - Mostrar esta ayuda"