-- =============================================================================
-- 09_indexes_explain.sql  |  Indexes and query plans
-- Re-runnable: drops and rebuilds its own objects.
--
-- With only ~40 tickets PostgreSQL always chooses a Seq Scan (reading the table is cheaper than
-- opening an index), so the before/after comparison is done on a generated table of 200 000 rows.
-- The timings you see will differ from machine to machine; what matters is the plan node
-- (Seq Scan -> Bitmap Index Scan) and the order of magnitude.
-- =============================================================================


SET client_min_messages = warning;   -- hide "does not exist, skipping" notices

-- ---- Large test table (random data) ---------------------------------------
DROP TABLE IF EXISTS tickets_test;

CREATE TABLE tickets_test AS
SELECT g                                               AS ticketid,
       1 + floor(random() * 1000)::int                 AS visitorid,
       1 + floor(random() * 20)::int                   AS exhibitionid,
       DATE '2024-01-01' + floor(random() * 1000)::int AS purchasedate,
       DATE '2024-01-01' + floor(random() * 1000)::int AS visitdate,
       round((10 + random() * 490)::numeric, 2)        AS price,
       (random() < 0.5)                                AS isused
FROM generate_series(1, 200000) AS g;

ANALYZE tickets_test;   -- refresh the statistics the planner uses


-- ---- EXPLAIN 1: before the index ------------------------------------------
-- EXPLAIN         = estimated plan only, the query is not run
-- EXPLAIN ANALYZE = the query really runs; adds actual time and row counts
EXPLAIN
SELECT * FROM tickets_test WHERE visitdate = DATE '2025-06-15';

EXPLAIN ANALYZE
SELECT * FROM tickets_test WHERE visitdate = DATE '2025-06-15';
-- expected: Seq Scan on tickets_test, "Rows Removed by Filter" close to 200 000


-- ---- Indexes on the real tables -------------------------------------------
-- Foreign keys are NOT indexed automatically in PostgreSQL (primary keys and UNIQUE are).
DROP INDEX IF EXISTS idx_tickets_visitdate, idx_tickets_visitorid,
                     idx_tickets_exhibition_visitdate, idx_tickets_price, idx_categories_name;

-- INDEX 1: a column that is often filtered on
CREATE INDEX idx_tickets_visitdate ON Tickets(VisitDate);

-- INDEX 2: a foreign key (speeds up joins and lookups by visitor)
CREATE INDEX idx_tickets_visitorid ON Tickets(VisitorID);

-- INDEX 3: composite; column order matters (helps WHERE ExhibitionID = ? [AND VisitDate ...])
CREATE INDEX idx_tickets_exhibition_visitdate ON Tickets(ExhibitionID, VisitDate);

-- INDEX 4: for sorting (ORDER BY Price DESC)
CREATE INDEX idx_tickets_price ON Tickets(Price DESC);

-- INDEX 5: unique, so two categories cannot share a name
CREATE UNIQUE INDEX idx_categories_name ON Categories(Name);


-- ---- EXPLAIN 2: same query after the index ---------------------------------
CREATE INDEX idx_tickets_test_visitdate ON tickets_test(visitdate);
ANALYZE tickets_test;

EXPLAIN
SELECT * FROM tickets_test WHERE visitdate = DATE '2025-06-15';

EXPLAIN ANALYZE
SELECT * FROM tickets_test WHERE visitdate = DATE '2025-06-15';
-- expected: Bitmap Index Scan on idx_tickets_test_visitdate, Execution Time far below the Seq Scan


-- ---- EXPLAIN 3: JOIN (small tables; Hash Join / Seq Scan is the right plan here) ----
EXPLAIN
SELECT e.Name, v.LastName, t.Price
FROM Tickets t
JOIN Visitors    v ON v.VisitorID    = t.VisitorID
JOIN Exhibitions e ON e.ExhibitionID = t.ExhibitionID;

EXPLAIN ANALYZE
SELECT e.Name, v.LastName, t.Price
FROM Tickets t
JOIN Visitors    v ON v.VisitorID    = t.VisitorID
JOIN Exhibitions e ON e.ExhibitionID = t.ExhibitionID;


-- ---- EXPLAIN 4: GROUP BY + HAVING (the Filter line under HashAggregate is the HAVING) ----
EXPLAIN
SELECT exhibitionid, COUNT(*) AS nr, SUM(price) AS total
FROM tickets_test
GROUP BY exhibitionid
HAVING SUM(price) > 100000;

EXPLAIN ANALYZE
SELECT exhibitionid, COUNT(*) AS nr, SUM(price) AS total
FROM tickets_test
GROUP BY exhibitionid
HAVING SUM(price) > 100000;


-- ---- EXPLAIN 5: ORDER BY on several columns (shows a Sort node) ----
EXPLAIN
SELECT * FROM tickets_test
ORDER BY exhibitionid, price DESC, visitdate;

EXPLAIN ANALYZE
SELECT * FROM tickets_test
ORDER BY exhibitionid, price DESC, visitdate;
