-- =============================================================================
-- 08_views.sql  |  Saved queries
-- A view stores the query, not the data: it always reflects the current tables.
-- Re-runnable (CREATE OR REPLACE).
-- =============================================================================

-- VIEW 1 (aggregation): tickets sold and revenue per exhibition
CREATE OR REPLACE VIEW v_exhibition_revenue AS
SELECT e.Name                AS Exhibition,
       COUNT(t.TicketID)     AS TicketCount,
       SUM(t.Price)          AS TotalRevenue
FROM Exhibitions e
JOIN Tickets t ON t.ExhibitionID = e.ExhibitionID
GROUP BY e.ExhibitionID, e.Name;

SELECT * FROM v_exhibition_revenue ORDER BY TotalRevenue DESC;


-- VIEW 2 (join of 3 tables): artifact details with artist and category
-- INNER JOINs, so artifacts without a category (e.g. 'Bird in Space') are not listed.
CREATE OR REPLACE VIEW v_artifact_details AS
SELECT a.Name                          AS Artifact,
       a.CreationYear,
       ar.FirstName || ' ' || ar.LastName AS Artist,
       c.Name                          AS Category,
       c.HistoricalPeriod
FROM Artifacts a
JOIN Artists    ar ON ar.ArtistID   = a.ArtistID
JOIN Categories c  ON c.CategoryID  = a.CategoryID;

SELECT * FROM v_artifact_details;


-- VIEW 3 (conditional filter on state + date): tickets still to be used
CREATE OR REPLACE VIEW v_active_tickets AS
SELECT TicketID, VisitorID, ExhibitionID, VisitDate, Price
FROM Tickets
WHERE IsUsed = FALSE
  AND VisitDate >= CURRENT_DATE;

SELECT * FROM v_active_tickets;


-- VIEW 4 (Top N): the five most expensive tickets
-- Ties at the cut-off are broken arbitrarily; add a second ORDER BY key for a stable result.
CREATE OR REPLACE VIEW v_top5_tickets AS
SELECT t.TicketID,
       v.FirstName || ' ' || v.LastName AS Visitor,
       t.Price
FROM Tickets t
JOIN Visitors v ON v.VisitorID = t.VisitorID
ORDER BY t.Price DESC, t.TicketID
LIMIT 5;

SELECT * FROM v_top5_tickets;


-- VIEW 5 (subquery in FROM): exhibitions whose revenue is above the average exhibition revenue
CREATE OR REPLACE VIEW v_exhibitions_above_average AS
SELECT g.ExhibitionID, g.Total
FROM (
    SELECT ExhibitionID, SUM(Price) AS Total
    FROM Tickets
    GROUP BY ExhibitionID
) AS g
WHERE g.Total > (
    SELECT AVG(s.Total)
    FROM (
        SELECT SUM(Price) AS Total
        FROM Tickets
        GROUP BY ExhibitionID
    ) AS s
);

SELECT * FROM v_exhibitions_above_average;
