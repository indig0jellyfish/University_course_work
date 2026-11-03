-- =============================================================================
-- 07_aggregates_subqueries.sql  |  Aggregate functions and subqueries
-- SUM / AVG / COUNT / MIN / MAX (5 each), 5 simple subqueries, 5 subqueries in FROM.
-- =============================================================================


-- ------------------------------------------------------------------ SUM -----
-- SUM 1: total of a column
SELECT SUM(Price) AS TotalRevenue FROM Tickets;

-- SUM 2: grouped (revenue per exhibition)
SELECT ExhibitionID, SUM(Price) AS RevenuePerExhibition
FROM Tickets
GROUP BY ExhibitionID;

-- SUM 3: sum of a product of two columns from different tables (price x exhibition length in days)
SELECT SUM(t.Price * (e.EndDate - e.StartDate)) AS PriceTimesDuration
FROM Tickets t
JOIN Exhibitions e ON e.ExhibitionID = t.ExhibitionID;

-- SUM 4: with a WHERE condition (revenue from tickets that were actually used)
SELECT SUM(Price) AS UsedTicketsRevenue
FROM Tickets
WHERE IsUsed = TRUE;

-- SUM 5: HAVING filters groups, not rows (exhibitions with more than 100 in revenue)
SELECT ExhibitionID, SUM(Price) AS Revenue
FROM Tickets
GROUP BY ExhibitionID
HAVING SUM(Price) > 100;


-- ------------------------------------------------------------------ AVG -----
-- AVG 1: overall average
SELECT AVG(Price) AS OverallAverage FROM Tickets;

-- AVG 2: per group
SELECT ExhibitionID, AVG(Price) AS AveragePerExhibition
FROM Tickets
GROUP BY ExhibitionID;

-- AVG 3: only for groups whose SUM exceeds a threshold (HAVING)
SELECT ExhibitionID, AVG(Price) AS Average
FROM Tickets
GROUP BY ExhibitionID
HAVING SUM(Price) > 100;

-- AVG 4: rows above the overall average (subquery)
SELECT *
FROM Tickets
WHERE Price > (SELECT AVG(Price) FROM Tickets);

-- AVG 5: average per exhibition, with the exhibition name (JOIN), rounded
SELECT e.Name, ROUND(AVG(t.Price), 2) AS AveragePrice
FROM Tickets t
JOIN Exhibitions e ON e.ExhibitionID = t.ExhibitionID
GROUP BY e.ExhibitionID, e.Name;


-- ---------------------------------------------------------------- COUNT -----
-- COUNT 1: number of rows
SELECT COUNT(*) AS TotalTickets FROM Tickets;

-- COUNT 2: number of distinct values
SELECT COUNT(DISTINCT Nationality) AS DistinctNationalities FROM Artists;

-- COUNT 3: rows of B per row of A (JOIN + GROUP BY): artifacts per category
SELECT c.Name AS Category, COUNT(a.ArtifactID) AS ArtifactCount
FROM Categories c
JOIN Artifacts a ON a.CategoryID = c.CategoryID
GROUP BY c.CategoryID, c.Name;

-- COUNT 4: NULLs in a nullable column (artists without a nationality)
SELECT COUNT(*) AS ArtistsWithoutNationality
FROM Artists
WHERE Nationality IS NULL;

-- COUNT 5: LEFT JOIN keeps groups with zero (tickets per exhibition, including 0)
-- COUNT(t.TicketID) ignores the NULLs the LEFT JOIN produces; COUNT(*) would report 1 instead of 0.
SELECT e.Name, COUNT(t.TicketID) AS TicketCount
FROM Exhibitions e
LEFT JOIN Tickets t ON t.ExhibitionID = e.ExhibitionID
GROUP BY e.ExhibitionID, e.Name;


-- ------------------------------------------------------------------ MIN -----
-- MIN 1
SELECT MIN(Price) AS MinPrice FROM Tickets;

-- MIN 2: per group
SELECT ExhibitionID, MIN(Price) AS MinPrice
FROM Tickets
GROUP BY ExhibitionID;

-- MIN 3: the whole row holding the minimum (subquery)
SELECT *
FROM Tickets
WHERE Price = (SELECT MIN(Price) FROM Tickets);

-- MIN 4: earliest date
SELECT MIN(PurchaseDate) AS FirstPurchase FROM Tickets;

-- MIN 5: groups whose minimum is above a threshold (HAVING)
SELECT ExhibitionID, MIN(Price) AS MinPrice
FROM Tickets
GROUP BY ExhibitionID
HAVING MIN(Price) > 90;


-- ------------------------------------------------------------------ MAX -----
-- MAX 1 (together with MIN)
SELECT MIN(Price) AS MinPrice, MAX(Price) AS MaxPrice FROM Tickets;

-- MAX 2: per group
SELECT ExhibitionID, MAX(Price) AS MaxPrice
FROM Tickets
GROUP BY ExhibitionID;

-- MAX 3: the whole row(s) holding the maximum (the most recently created artifact)
SELECT *
FROM Artifacts
WHERE CreationYear = (SELECT MAX(CreationYear) FROM Artifacts);

-- MAX 4: latest date
SELECT MAX(VisitDate) AS LastVisit FROM Tickets;

-- MAX 5: most expensive ticket per exhibition, with the exhibition name (JOIN)
SELECT e.Name, MAX(t.Price) AS MaxPrice
FROM Exhibitions e
JOIN Tickets t ON t.ExhibitionID = e.ExhibitionID
GROUP BY e.ExhibitionID, e.Name;


-- ------------------------------------------------- SIMPLE SUBQUERIES -------
-- SQ 1: = (SELECT MAX/MIN ...) : the oldest artists by birth year
SELECT *
FROM Artists
WHERE BirthYear = (SELECT MIN(BirthYear) FROM Artists);

-- SQ 2: IN + GROUP BY/HAVING inside the subquery: artifacts of artists with more than one artifact
SELECT *
FROM Artifacts
WHERE ArtistID IN (
    SELECT ArtistID
    FROM Artifacts
    GROUP BY ArtistID
    HAVING COUNT(*) > 1
);

-- SQ 3: NOT EXISTS: artists with no artifacts
-- (NOT EXISTS is safer than NOT IN, which returns nothing if the subquery contains a NULL)
SELECT *
FROM Artists ar
WHERE NOT EXISTS (
    SELECT 1 FROM Artifacts a WHERE a.ArtistID = ar.ArtistID
);

-- SQ 4: subquery in SELECT: each ticket next to the overall average
SELECT TicketID, Price, (SELECT AVG(Price) FROM Tickets) AS OverallAverage
FROM Tickets;

-- SQ 5: EXISTS: visitors with at least one used ticket
SELECT *
FROM Visitors v
WHERE EXISTS (
    SELECT 1 FROM Tickets t
    WHERE t.VisitorID = v.VisitorID AND t.IsUsed = TRUE
);


-- ----------------------------------------------- SUBQUERIES IN FROM --------
-- FROM 1: average after filtering inside the derived table (tickets above 100)
SELECT AVG(t1.Price) AS FilteredAverage
FROM (SELECT Price FROM Tickets WHERE Price > 100) AS t1;

-- FROM 2: aggregate over an aggregate (total of the per-exhibition totals)
SELECT SUM(g.Total) AS GrandTotal
FROM (
    SELECT ExhibitionID, SUM(Price) AS Total
    FROM Tickets
    GROUP BY ExhibitionID
) AS g;

-- FROM 3: the exhibitions with the highest and the lowest total revenue
SELECT g.ExhibitionID, g.Total
FROM (
    SELECT ExhibitionID, SUM(Price) AS Total
    FROM Tickets
    GROUP BY ExhibitionID
) AS g
JOIN (
    SELECT MAX(s.Total) AS Mx, MIN(s.Total) AS Mn
    FROM (
        SELECT SUM(Price) AS Total
        FROM Tickets
        GROUP BY ExhibitionID
    ) AS s
) AS m ON g.Total IN (m.Mx, m.Mn);

-- FROM 4: each exhibition's share of total revenue (derived table + one-row CROSS JOIN for the total)
-- 100.0 forces decimal division; with integers PostgreSQL would truncate.
SELECT g.ExhibitionID, g.Total,
       ROUND(100.0 * g.Total / t.TotalGeneral, 2) AS Percent
FROM (
    SELECT ExhibitionID, SUM(Price) AS Total
    FROM Tickets
    GROUP BY ExhibitionID
) AS g
CROSS JOIN (SELECT SUM(Price) AS TotalGeneral FROM Tickets) AS t;

-- FROM 5: average number of artifacts per artist
SELECT ROUND(AVG(x.ArtifactCount), 2) AS AvgArtifactsPerArtist
FROM (
    SELECT ArtistID, COUNT(*) AS ArtifactCount
    FROM Artifacts
    GROUP BY ArtistID
) AS x;
