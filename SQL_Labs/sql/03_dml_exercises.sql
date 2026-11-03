-- =============================================================================
-- 03_dml_exercises.sql  |  UPDATE and DELETE exercises
-- Safe to re-run: everything runs inside one transaction that ends with ROLLBACK,
-- so the sample data from 02_seed.sql is left untouched.
-- Do NOT paste these statements one by one into an auto-commit session unless you want them applied.
-- Each UPDATE has a WHERE clause; the four WHERE styles are: unique row, range, logic, NULL.
-- =============================================================================

BEGIN;

-- UPDATE exercises

-- 2.1 UPDATE Artists
-- 1. Unique row, by primary key
UPDATE Artists
SET Nationality = 'French'
WHERE ArtistID = 1;

-- 2. Range, numeric condition
UPDATE Artists
SET Nationality = 'Dutch'
WHERE BirthYear < 1860;

-- 3. Logic, two conditions combined
UPDATE Artists
SET Nationality = 'European'
WHERE BirthYear < 1900
  AND Nationality IS NOT NULL;

-- 4. NULL values
UPDATE Artists
SET Nationality = 'Unknown'
WHERE Nationality IS NULL;

-- 5. Single-row change
UPDATE Artists
SET FirstName = 'Pablo'
WHERE ArtistID = 3;



-- 2.2 UPDATE Categories
UPDATE Categories
SET Description = 'Category dedicated to Impressionist paintings.'
WHERE CategoryID = 1;

UPDATE Categories
SET ObjectType = 'Painting'
WHERE CategoryID > 2;

UPDATE Categories
SET Description = 'Modern category for geometric art.'
WHERE HistoricalPeriod = '20th Century'
  AND ObjectType = 'Painting';

UPDATE Categories
SET HistoricalPeriod = 'Modern Period'
WHERE HistoricalPeriod IS NULL;

UPDATE Categories
SET Name = 'Modern Sculpture Updated'
WHERE CategoryID = 5;


-- 2.3 UPDATE Exhibitions
UPDATE Exhibitions
SET Description = 'An exhibition about light, colour and nature.'
WHERE ExhibitionID = 1;

UPDATE Exhibitions
SET Description = 'Extended European exhibition.'
WHERE ExhibitionID > 2;

UPDATE Exhibitions
SET EndDate = EndDate + INTERVAL '5 days' 
WHERE StartDate >= '2026-06-01'
  AND EndDate < '2027-01-01';

UPDATE Exhibitions
SET Description = 'Updated description.'
WHERE Description IS NULL;

UPDATE Exhibitions
SET Name = 'Women in European Art'
WHERE ExhibitionID = 4;


-- 2.4 UPDATE Visitors
UPDATE Visitors
SET PhoneNumber = '060111111'
WHERE VisitorID = 1;

UPDATE Visitors
SET PhoneNumber = '060222222'
WHERE VisitorID > 3;

UPDATE Visitors
SET PhoneNumber = '060333333'
WHERE BirthDate < '2000-01-01'
  AND PhoneNumber IS NOT NULL;

UPDATE Visitors
SET PhoneNumber = 'Unknown'
WHERE PhoneNumber IS NULL;

UPDATE Visitors
SET LastName = 'Popescu-Updated'
WHERE VisitorID = 1;



-- 2.5 UPDATE Artifacts
UPDATE Artifacts
SET Description = 'Famous Impressionist painting.'
WHERE ArtifactID = 1;

UPDATE Artifacts
SET Description = 'Work created in the 19th century.'
WHERE CreationYear < 1900;

UPDATE Artifacts
SET Description = 'Modern European work.'
WHERE CreationYear >= 1900
  AND ArtistID > 2;

UPDATE Artifacts
SET Description = 'Unknown description'
WHERE Description IS NULL;

UPDATE Artifacts
SET Name = 'Starry Night Updated'
WHERE ArtifactID = 2;



-- 2.6 UPDATE ExhibitionArtifacts
UPDATE ExhibitionArtifacts
SET DisplayEndDate = '2026-03-20'
WHERE ExhibitionArtifactID = 1;

UPDATE ExhibitionArtifacts
SET DisplayEndDate = DisplayEndDate + INTERVAL '3 days'
WHERE ExhibitionID > 2;

UPDATE ExhibitionArtifacts
SET DisplayStartDate = DisplayStartDate + INTERVAL '1 day'
WHERE ExhibitionID >= 3
  AND ArtifactID >= 3;

UPDATE ExhibitionArtifacts
SET DisplayEndDate = DisplayStartDate + INTERVAL '30 days'
WHERE DisplayEndDate IS NULL;

UPDATE ExhibitionArtifacts
SET DisplayEndDate = '2026-05-25'
WHERE ExhibitionArtifactID = 2;



-- 2.7 UPDATE Tickets
UPDATE Tickets
SET Price = 105.00
WHERE TicketID = 1;

UPDATE Tickets
SET Price = Price + 10
WHERE Price > 120;

UPDATE Tickets
SET IsUsed = TRUE
WHERE Price > 100
  AND VisitDate < '2026-09-01';

UPDATE Tickets
SET IsUsed = FALSE
WHERE IsUsed IS NULL;

UPDATE Tickets
SET Price = 125.00
WHERE TicketID = 2;


-- =============================================================================
-- DELETE exercises
-- Rows are deleted in child -> parent order. Temporary "Test" rows are created first so
-- that no real data is the target of the exercise. Ids are looked up, never hard-coded
-- (sequences do not roll back, so an id like 6 is not guaranteed to be the test row).
-- =============================================================================

-- 3.1 Test data
INSERT INTO Artists (FirstName, LastName, BirthYear, Nationality)
VALUES ('Test', 'Artist', 2000, 'Test');

INSERT INTO Categories (Name, Description, HistoricalPeriod, ObjectType)
VALUES ('Test Category', 'Category used to test DELETE.', 'Test Period', 'Test');

INSERT INTO Exhibitions (Name, Description, StartDate, EndDate)
VALUES ('Test Exhibition', 'Exhibition used to test DELETE.', '2027-02-01', '2027-02-10');

INSERT INTO Visitors (FirstName, LastName, Email, PhoneNumber, BirthDate)
VALUES ('Test', 'Visitor', 'test.visitor@example.com', '060999999', '2000-01-01');


-- 3.2 DELETE Artists
-- single row, by primary key
DELETE FROM Artists
WHERE ArtistID = (SELECT ArtistID FROM Artists WHERE FirstName = 'Test' AND LastName = 'Artist');

-- bulk, by condition
DELETE FROM Artists WHERE Nationality = 'Test';

DELETE FROM Artists WHERE FirstName = 'Test';

DELETE FROM Artists WHERE LastName = 'Test';

-- matches nothing: safe no-op
DELETE FROM Artists WHERE ArtistID = 9999;


-- 3.3 DELETE Categories
DELETE FROM Categories
WHERE CategoryID = (SELECT CategoryID FROM Categories WHERE Name = 'Test Category');

DELETE FROM Categories WHERE Name = 'Test Category';

DELETE FROM Categories WHERE ObjectType = 'Test';

DELETE FROM Categories WHERE HistoricalPeriod = 'Test Period';

DELETE FROM Categories WHERE CategoryID = 9999;


-- 3.4 DELETE Exhibitions
DELETE FROM Exhibitions
WHERE ExhibitionID = (SELECT ExhibitionID FROM Exhibitions WHERE Name = 'Test Exhibition');

DELETE FROM Exhibitions WHERE Name = 'Test Exhibition';

DELETE FROM Exhibitions WHERE StartDate > '2027-01-01';

DELETE FROM Exhibitions WHERE Description = 'Exhibition used to test DELETE.';

DELETE FROM Exhibitions WHERE ExhibitionID = 9999;


-- 3.5 DELETE Visitors
DELETE FROM Visitors
WHERE VisitorID = (SELECT VisitorID FROM Visitors WHERE Email = 'test.visitor@example.com');

DELETE FROM Visitors WHERE Email = 'test.visitor@example.com';

DELETE FROM Visitors WHERE FirstName = 'Test';

DELETE FROM Visitors WHERE LastName = 'Visitor';

DELETE FROM Visitors WHERE VisitorID = 9999;


-- 3.6 DELETE Artifacts
INSERT INTO Artifacts (Name, Description, CreationYear, ArtistID, CategoryID) VALUES
    ('Test Artifact 1', 'Test', 2020, 1, 1),
    ('Test Artifact 2', 'Test', 2021, 1, 1),
    ('Test Artifact 3', 'Test', 2022, 2, 2),
    ('Test Artifact 4', 'Test', 2023, 3, 3),
    ('Test Artifact 5', 'Test', 2024, 4, 4);

DELETE FROM Artifacts WHERE Name = 'Test Artifact 1';

DELETE FROM Artifacts WHERE Name LIKE 'Test Artifact%';

DELETE FROM Artifacts WHERE Description = 'Test';

DELETE FROM Artifacts WHERE CreationYear >= 2020 AND Name LIKE 'Test%';

DELETE FROM Artifacts WHERE ArtifactID = 9999;


-- 3.7 DELETE ExhibitionArtifacts
-- A pair that does not exist yet (the seed data already has Water Lilies in Light and Color,
-- and the table has UNIQUE (ExhibitionID, ArtifactID)).
INSERT INTO ExhibitionArtifacts (ExhibitionID, ArtifactID, DisplayStartDate, DisplayEndDate)
SELECT e.ExhibitionID, a.ArtifactID, DATE '2026-01-20', DATE '2026-02-20'
FROM Exhibitions e, Artifacts a
WHERE e.Name = 'Light and Color' AND a.Name = 'Starry Night';

-- single row, by primary key
DELETE FROM ExhibitionArtifacts
WHERE ExhibitionArtifactID = (SELECT MAX(ExhibitionArtifactID) FROM ExhibitionArtifacts);

DELETE FROM ExhibitionArtifacts WHERE DisplayStartDate > '2027-01-01';

DELETE FROM ExhibitionArtifacts WHERE DisplayEndDate < '2025-01-01';

DELETE FROM ExhibitionArtifacts WHERE ExhibitionID = 9999;

DELETE FROM ExhibitionArtifacts WHERE ArtifactID = 9999;


-- 3.8 DELETE Tickets
INSERT INTO Visitors (FirstName, LastName, Email, PhoneNumber, BirthDate)
VALUES ('Delete', 'TestVisitor', 'delete.test@example.com', '060888888', '2000-01-01');

INSERT INTO Tickets (VisitorID, ExhibitionID, VisitDate, Price)
VALUES (
    (SELECT VisitorID FROM Visitors WHERE Email = 'delete.test@example.com'),
    1,
    '2026-02-15',
    50.00
);

-- single row, by primary key
DELETE FROM Tickets
WHERE TicketID = (
    SELECT MAX(TicketID) FROM Tickets
    WHERE VisitorID = (SELECT VisitorID FROM Visitors WHERE Email = 'delete.test@example.com')
);

-- NOTE: the two bulk deletes below also match REAL tickets in the seed data
-- (e.g. unused tickets under 100). That is harmless only because this whole file
-- is rolled back at the end.
DELETE FROM Tickets WHERE Price < 60;

DELETE FROM Tickets WHERE IsUsed = FALSE AND Price < 100;

DELETE FROM Tickets
WHERE VisitorID = (SELECT VisitorID FROM Visitors WHERE Email = 'delete.test@example.com');

DELETE FROM Tickets WHERE TicketID = 9999;

DELETE FROM Visitors WHERE Email = 'delete.test@example.com';

-- Undo everything above.
ROLLBACK;
