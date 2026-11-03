-- =============================================================================
-- 10_metadata.sql  |  The database describing itself
-- information_schema.tables / information_schema.columns / pg_indexes.
-- Always filter on the schema ('public'), otherwise PostgreSQL's own catalogs are returned too.
-- Table and column names are stored in lower case.
-- =============================================================================


-- ---- information_schema.tables --------------------------------------------
-- TABLES 1: all base tables in the public schema
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
ORDER BY table_name;

-- TABLES 2: all views
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public' AND table_type = 'VIEW';

-- TABLES 3: how many tables
SELECT COUNT(*) AS TableCount
FROM information_schema.tables
WHERE table_schema = 'public' AND table_type = 'BASE TABLE';

-- TABLES 4: tables whose name starts with a given letter
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public' AND table_name LIKE 'a%';

-- TABLES 5: schema, name and type of everything
SELECT table_schema, table_name, table_type
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_type, table_name;


-- ---- information_schema.columns -------------------------------------------
-- COLUMNS 1: columns and data types of one table, in table order
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_schema = 'public' AND table_name = 'tickets'
ORDER BY ordinal_position;

-- COLUMNS 2: every integer column
SELECT table_name, column_name
FROM information_schema.columns
WHERE table_schema = 'public' AND data_type = 'integer'
ORDER BY table_name, ordinal_position;

-- COLUMNS 3: columns with "id" in the name (candidate keys). Note: _ in LIKE means "any single
-- character"; use '%id\_%' to match a literal underscore.
SELECT table_name, column_name
FROM information_schema.columns
WHERE table_schema = 'public' AND column_name LIKE '%id%'
ORDER BY table_name;

-- COLUMNS 4: how many columns a table has
SELECT COUNT(*) AS ColumnCount
FROM information_schema.columns
WHERE table_schema = 'public' AND table_name = 'visitors';

-- COLUMNS 5: columns that allow NULL
SELECT table_name, column_name
FROM information_schema.columns
WHERE table_schema = 'public' AND is_nullable = 'YES'
ORDER BY table_name;


-- ---- pg_indexes (PostgreSQL specific) -------------------------------------
-- PG_INDEXES 1: all indexes in the public schema
SELECT tablename, indexname, indexdef
FROM pg_indexes
WHERE schemaname = 'public'
ORDER BY tablename, indexname;

-- PG_INDEXES 2: indexes of one table
SELECT indexname, indexdef
FROM pg_indexes
WHERE schemaname = 'public' AND tablename = 'tickets';

-- PG_INDEXES 3: how many indexes in total
SELECT COUNT(*) AS IndexCount
FROM pg_indexes
WHERE schemaname = 'public';

-- PG_INDEXES 4: definitions of the non-unique indexes
SELECT indexname, indexdef
FROM pg_indexes
WHERE schemaname = 'public' AND indexdef NOT LIKE '%UNIQUE%';

-- PG_INDEXES 5: indexes with their table, ordered by table name
SELECT tablename, indexname
FROM pg_indexes
WHERE schemaname = 'public'
ORDER BY tablename;
