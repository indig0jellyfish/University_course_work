-- =============================================================================
-- 04_select_basics.sql  |  SELECT, WHERE, DISTINCT, ORDER BY, LIMIT
-- Five query shapes per table: simple, 3 columns, filtered, DISTINCT, ordered;
-- then LIMIT and combined forms.
-- =============================================================================

-- 4. SELECT
-- 4.1 SELECT, Artists
SELECT *
FROM Artists;

-- only 3 columns
SELECT FirstName, LastName, Nationality
FROM Artists;

-- WHERE with a comparison operator
SELECT *
FROM Artists
WHERE BirthYear < 1900;

-- DISTINCT
SELECT DISTINCT Nationality
FROM Artists;

-- ORDER BY DESC
SELECT *
FROM Artists
ORDER BY BirthYear DESC;



-- 4.2 SELECT, Categories
SELECT *
FROM Categories;

-- 3 columns
SELECT Name, HistoricalPeriod, ObjectType
FROM Categories;

-- WHERE
SELECT *
FROM Categories
WHERE CategoryID > 2;

-- DISTINCT
SELECT DISTINCT ObjectType
FROM Categories;

-- ORDER BY
SELECT *
FROM Categories
ORDER BY CategoryID DESC;



-- 4.3 SELECT - Exhibitions
-- SELECT 1
SELECT *
FROM Exhibitions;

-- SELECT 2
SELECT Name, StartDate, EndDate
FROM Exhibitions;

-- WHERE
SELECT *
FROM Exhibitions
WHERE StartDate >= '2026-06-01';

-- DISTINCT
SELECT DISTINCT Name
FROM Exhibitions;

-- ORDER BY
SELECT *
FROM Exhibitions
ORDER BY StartDate DESC;



-- 4.4 SELECT - Visitors
-- SELECT 1
SELECT *
FROM Visitors;

-- SELECT 2
SELECT FirstName, LastName, Email
FROM Visitors;

-- WHERE
SELECT *
FROM Visitors
WHERE BirthDate < '2000-01-01';

-- DISTINCT
SELECT DISTINCT LastName
FROM Visitors;

-- ORDER BY
SELECT *
FROM Visitors
ORDER BY BirthDate DESC;



-- 4.5 SELECT - Artifacts
-- SELECT 1
SELECT *
FROM Artifacts;

-- SELECT 2
SELECT Name, CreationYear, ArtistID
FROM Artifacts;

-- WHERE
SELECT *
FROM Artifacts
WHERE CreationYear > 1900;

-- DISTINCT
SELECT DISTINCT Name
FROM Artifacts;

-- ORDER BY
SELECT *
FROM Artifacts
ORDER BY CreationYear DESC;



-- 4.6 SELECT - ExhibitionArtifacts
-- SELECT 1
SELECT *
FROM ExhibitionArtifacts;

-- SELECT 2
SELECT ExhibitionID, ArtifactID, DisplayStartDate
FROM ExhibitionArtifacts;

-- WHERE
SELECT *
FROM ExhibitionArtifacts
WHERE ExhibitionID > 2;

-- DISTINCT
SELECT DISTINCT ExhibitionID
FROM ExhibitionArtifacts;

-- ORDER BY
SELECT *
FROM ExhibitionArtifacts
ORDER BY DisplayStartDate DESC;



-- 4.7 SELECT - Tickets
-- SELECT 1
SELECT *
FROM Tickets;

-- SELECT 2
SELECT VisitorID, ExhibitionID, Price
FROM Tickets;

-- WHERE
SELECT *
FROM Tickets
WHERE Price > 100;

-- DISTINCT
SELECT DISTINCT Price
FROM Tickets;

-- ORDER BY
SELECT *
FROM Tickets
ORDER BY Price DESC;



-- 5. Additional SELECTs
-- LIMIT 3
SELECT *
FROM Artists
LIMIT 3;

-- WHERE + ORDER BY
SELECT *
FROM Artists
WHERE BirthYear < 1900
ORDER BY BirthYear ASC;

-- most recent: ORDER BY DESC + LIMIT 1
SELECT *
FROM Exhibitions
ORDER BY StartDate DESC
LIMIT 1;

-- oldest: ORDER BY ASC + LIMIT 5
SELECT *
FROM Exhibitions
ORDER BY StartDate ASC
LIMIT 5;

-- VARCHAR + ORDER BY + LIMIT
SELECT *
FROM Artists
WHERE Nationality = 'French'
ORDER BY LastName ASC
LIMIT 3;
