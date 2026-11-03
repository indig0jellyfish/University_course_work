-- Runs the whole project in order. From the repository root:
--   psql -h localhost -U museum -d museum -f sql/run_all.sql
-- \ir resolves paths relative to this file. The script stops at the first error.
\set ON_ERROR_STOP on

\ir 01_schema.sql
\ir 02_seed.sql
\ir 03_dml_exercises.sql
\ir 04_select_basics.sql
\ir 05_joins.sql
\ir 06_operators.sql
\ir 07_aggregates_subqueries.sql
\ir 08_views.sql
\ir 09_indexes_explain.sql
\ir 10_metadata.sql
