-- Create extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Grant privileges to the user
GRANT ALL PRIVILEGES ON DATABASE notion_db TO postgres;

-- Connect to the database
\connect notion_db

-- Additional initialization can be added here
-- For example:
-- CREATE SCHEMA IF NOT EXISTS app;
-- GRANT ALL ON SCHEMA app TO postgres; 