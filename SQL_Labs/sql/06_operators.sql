-- =============================================================================
-- 06_operators.sql  |  WHERE operators
-- AND, OR, NOT, comparison, BETWEEN, LIKE / ILIKE, IN, EXISTS, IS [NOT] NULL,
-- then combinations with JOINs.
-- =============================================================================

-- AND
SELECT *
FROM Artists
WHERE BirthYear > 1800
  AND BirthYear < 1900;

SELECT *
FROM Artifacts
WHERE CreationYear > 1900
  AND ArtistID > 2;

SELECT *
FROM Tickets
WHERE Price > 100
  AND IsUsed = TRUE;

SELECT *
FROM Exhibitions
WHERE StartDate >= '2026-01-01'
  AND EndDate <= '2026-12-31';

SELECT *
FROM Visitors
WHERE BirthDate >= '2000-01-01'
  AND BirthDate <= '2005-12-31';

-- OR
SELECT *
FROM Artists
WHERE Nationality = 'French'
   OR Nationality = 'Dutch';

SELECT *
FROM Categories
WHERE ObjectType = 'Painting'
   OR ObjectType = 'Sculpture';

SELECT *
FROM Artifacts
WHERE CreationYear < 1900
   OR CreationYear > 1930;

SELECT *
FROM Tickets
WHERE Price < 110
   OR Price > 140;

SELECT *
FROM Visitors
WHERE FirstName = 'Ana'
   OR FirstName = 'Maria';

-- NOT
SELECT *
FROM Artists
WHERE NOT Nationality = 'French';

SELECT *
FROM Categories
WHERE NOT ObjectType = 'Sculpture';

SELECT *
FROM Artifacts
WHERE NOT CreationYear < 1900;

SELECT *
FROM Tickets
WHERE NOT IsUsed;

SELECT *
FROM Visitors
WHERE NOT FirstName = 'Ana';

-- COMPARISON (=, !=, >, <)
SELECT * FROM Artists
WHERE ArtistID = 1;

SELECT * FROM Categories
WHERE CategoryID = 1;

SELECT * FROM Exhibitions
WHERE ExhibitionID = 1;

SELECT * FROM Artifacts
WHERE ArtifactID = 1;

SELECT * FROM Tickets
WHERE TicketID = 1;

SELECT * FROM Artists
WHERE BirthYear != 1907;

SELECT * FROM Categories
WHERE ObjectType != 'Sculpture';

SELECT * FROM Exhibitions
WHERE ExhibitionID != 1;

SELECT * FROM Artifacts
WHERE CreationYear != 1937;

SELECT * FROM Tickets
WHERE Price != 100;

SELECT * FROM Artists
WHERE BirthYear > 1850;

SELECT * FROM Categories
WHERE CategoryID > 2;

SELECT * FROM Exhibitions
WHERE ExhibitionID > 2;

SELECT * FROM Artifacts
WHERE CreationYear > 1900;

SELECT * FROM Tickets
WHERE Price > 100;

SELECT * FROM Artists
WHERE BirthYear < 1900;

SELECT * FROM Categories
WHERE CategoryID < 4;

SELECT * FROM Exhibitions
WHERE ExhibitionID < 4;

SELECT * FROM Artifacts
WHERE CreationYear < 1900;

SELECT * FROM Tickets
WHERE Price < 130;

-- BETWEEN
SELECT *
FROM Artists
WHERE BirthYear BETWEEN 1800 AND 1900;

SELECT *
FROM Categories
WHERE CategoryID BETWEEN 1 AND 4;

SELECT *
FROM Exhibitions
WHERE StartDate BETWEEN '2026-01-01' AND '2026-06-30';

SELECT *
FROM Artifacts
WHERE CreationYear BETWEEN 1880 AND 1940;

SELECT *
FROM Tickets
WHERE Price BETWEEN 100 AND 130;

-- LIKE 1
SELECT *
FROM Artists
WHERE LastName LIKE 'P%';

SELECT *
FROM Categories
WHERE Name LIKE '%ism%';   -- Impressionism, Cubism, Surrealism, ...

SELECT *
FROM Exhibitions
WHERE Name LIKE '%Art%';

SELECT *
FROM Artifacts
WHERE Name LIKE '%Star%';

SELECT *
FROM Visitors
WHERE LastName LIKE 'C%';

-- ILIKE 
SELECT *
FROM Artists
WHERE LastName ILIKE 'p%';

SELECT *
FROM Categories
WHERE Name ILIKE '%ISM%';  -- case-insensitive: same rows as above

SELECT *
FROM Exhibitions
WHERE Name ILIKE '%ART%';

SELECT *
FROM Artifacts
WHERE Name ILIKE '%star%';

SELECT *
FROM Visitors
WHERE LastName ILIKE 'c%';

-- IN 
SELECT *
FROM Artists
WHERE Nationality IN ('French', 'Dutch', 'Spanish');

SELECT *
FROM Categories
WHERE ObjectType IN ('Painting', 'Sculpture');

SELECT *
FROM Exhibitions
WHERE ExhibitionID IN (1, 3, 5);

SELECT *
FROM Artifacts
WHERE ArtistID IN (1, 2, 3);

SELECT *
FROM Tickets
WHERE Price IN (105, 125, 150);

-- EXISTS 
SELECT *
FROM Artists a
WHERE EXISTS (
    SELECT 1
    FROM Artifacts ar
    WHERE ar.ArtistID = a.ArtistID
);

SELECT *
FROM Categories c
WHERE EXISTS (
    SELECT 1
    FROM Artifacts ar
    WHERE ar.CategoryID = c.CategoryID
);

SELECT *
FROM Exhibitions e
WHERE EXISTS (
    SELECT 1
    FROM ExhibitionArtifacts ea
    WHERE ea.ExhibitionID = e.ExhibitionID
);

SELECT *
FROM Visitors v
WHERE EXISTS (
    SELECT 1
    FROM Tickets t
    WHERE t.VisitorID = v.VisitorID
);

SELECT *
FROM Artifacts ar
WHERE EXISTS (
    SELECT 1
    FROM ExhibitionArtifacts ea
    WHERE ea.ArtifactID = ar.ArtifactID
);

-- IS NULL 
SELECT *
FROM Artists
WHERE MentorID IS NULL;

SELECT *
FROM Artifacts
WHERE CategoryID IS NULL;

SELECT *
FROM Artists
WHERE Nationality IS NULL;

SELECT *
FROM Artists
WHERE MentorID IS NOT NULL;

SELECT *
FROM Artifacts
WHERE CategoryID IS NOT NULL;

SELECT *
FROM Visitors
WHERE PhoneNumber IS NOT NULL;

-- JOIN + AND + BETWEEN
SELECT
    a.FirstName || ' ' || a.LastName AS Artist,
    ar.Name AS Artifact,
    ar.CreationYear
FROM Artists a
INNER JOIN Artifacts ar
    ON a.ArtistID = ar.ArtistID
WHERE ar.CreationYear BETWEEN 1880 AND 1940
  AND a.BirthYear < 1900;

-- JOIN + OR + IN
SELECT
    a.FirstName || ' ' || a.LastName AS Artist,
    ar.Name AS Artifact
FROM Artists a
INNER JOIN Artifacts ar
    ON a.ArtistID = ar.ArtistID
WHERE a.Nationality IN ('French', 'Dutch')
   OR ar.CreationYear > 1930;

-- JOIN + LIKE + >
SELECT
    a.LastName,
    ar.Name,
    ar.CreationYear
FROM Artists a
INNER JOIN Artifacts ar
    ON a.ArtistID = ar.ArtistID
WHERE a.LastName LIKE 'P%'
  AND ar.CreationYear > 1900;

-- LEFT JOIN + IS NULL
SELECT
    ar.Name AS Artifact,
    c.Name AS Category
FROM Artifacts ar
LEFT JOIN Categories c
    ON ar.CategoryID = c.CategoryID
WHERE c.CategoryID IS NULL;

-- LEFT JOIN + NOT
SELECT
    v.FirstName,
    v.LastName,
    t.Price
FROM Visitors v
LEFT JOIN Tickets t
    ON v.VisitorID = t.VisitorID
WHERE NOT (t.Price > 130);

-- JOIN + ILIKE + BETWEEN
SELECT
    e.Name AS Exhibition,
    t.Price,
    t.VisitDate
FROM Exhibitions e
INNER JOIN Tickets t
    ON e.ExhibitionID = t.ExhibitionID
WHERE e.Name ILIKE '%art%'
  AND t.Price BETWEEN 100 AND 150;
