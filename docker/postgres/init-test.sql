-- Test database initialization script

-- Create test database if not exists
SELECT 'CREATE DATABASE test_career_db'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'test_career_db');

-- Connect to test database
\c test_career_db;

-- Create test user with necessary permissions
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'test_user') THEN
        CREATE USER test_user WITH PASSWORD 'test_password';
    END IF;
END
$$;

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE test_career_db TO test_user;
GRANT ALL ON SCHEMA public TO test_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO test_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO test_user;

-- Create extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Test data setup (optional)
-- This will be populated by the application's test fixtures