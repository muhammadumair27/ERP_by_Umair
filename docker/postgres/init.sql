-- =============================================================================
-- Manufacturing ERP - PostgreSQL bootstrap
-- Executed once, on first initialisation of the data volume.
-- Runs as the superuser defined by POSTGRES_USER.
-- =============================================================================

-- Trigram matching, used by the searchable master-data endpoints.
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Accent-insensitive search.
CREATE EXTENSION IF NOT EXISTS unaccent;

-- GIN indexing for composite queries over scalar columns.
CREATE EXTENSION IF NOT EXISTS btree_gin;
