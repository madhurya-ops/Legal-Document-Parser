-- LegalDoc Database Initialization Script
-- This script sets up the initial database configuration and optimizations

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create indexes for performance optimization
-- Note: Tables will be created by SQLAlchemy, this script just adds optimizations

-- Function to create performance indexes after tables are created
CREATE OR REPLACE FUNCTION create_performance_indexes() RETURNS void AS $$
BEGIN
    -- Check if tables exist before creating indexes
    IF EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'users') THEN
        -- User table indexes
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_email_active 
        ON users(email, is_active) WHERE is_active = true;
        
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_username_lower 
        ON users(LOWER(username));
        
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_created_at 
        ON users(created_at DESC);
    END IF;

    IF EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'documents') THEN
        -- Document table indexes
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_documents_user_created 
        ON documents(user_id, created_at DESC);
        
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_documents_file_hash 
        ON documents(file_hash);
        
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_documents_file_type 
        ON documents(file_type);
    END IF;

    -- Performance settings
    PERFORM set_config('shared_preload_libraries', 'pg_stat_statements', false);
    
END;
$$ LANGUAGE plpgsql;

-- Create a function to maintain database performance
CREATE OR REPLACE FUNCTION maintain_database() RETURNS void AS $$
BEGIN
    -- Update table statistics
    ANALYZE;
    
    -- Log the maintenance
    RAISE NOTICE 'Database maintenance completed at %', NOW();
END;
$$ LANGUAGE plpgsql;

-- Set up database configuration for better performance
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET random_page_cost = 1.1;
ALTER SYSTEM SET checkpoint_completion_target = 0.9;
ALTER SYSTEM SET wal_buffers = '16MB';
ALTER SYSTEM SET default_statistics_target = 100;

-- Log completion
DO $$
BEGIN
    RAISE NOTICE 'LegalDoc database initialization completed successfully';
    RAISE NOTICE 'Database: %, User: %', current_database(), current_user;
    RAISE NOTICE 'Time: %', NOW();
END;
$$;
