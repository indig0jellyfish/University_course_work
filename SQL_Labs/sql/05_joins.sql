-- =============================================================================
-- 05_joins.sql  |  INNER, LEFT, RIGHT, FULL OUTER and SELF JOIN
-- What the seed data gives the OUTER JOINs to find:
--   - Artifacts.CategoryID is nullable and 'Bird in Space' has no category
--   - the 'Photography' category has no artifacts
--   - 'Swans Reflecting Elephants' is in no exhibition; 'Photography Now' has no artifacts or tickets
--   - two visitors have no tickets
-- SELF JOIN uses Artists.MentorID (artist -> mentor).
-- =============================================================================

-- INNER JOIN 
SELECT
    a.FirstName,
    a.LastName,
    ar.Name AS Artifact
FROM Artists a
INNER JOIN Artifacts ar
    ON a.ArtistID = ar.ArtistID;

SELECT
    c.Name AS Category,
    ar.Name AS Artifact
FROM Categories c
INNER JOIN Artifacts ar
    ON c.CategoryID = ar.CategoryID;

SELECT
    e.Name AS Exhibition,
    ea.ArtifactID
FROM Exhibitions e
INNER JOIN ExhibitionArtifacts ea
    ON e.ExhibitionID = ea.ExhibitionID;

SELECT
    ar.Name AS Artifact,
    ea.ExhibitionID,
    ea.DisplayStartDate
FROM Artifacts ar
INNER JOIN ExhibitionArtifacts ea
    ON ar.ArtifactID = ea.ArtifactID;

SELECT
    v.FirstName,
    v.LastName,
    t.Price
FROM Visitors v
INNER JOIN Tickets t
    ON v.VisitorID = t.VisitorID;

SELECT
    e.Name AS Exhibition,
    t.VisitDate,
    t.Price
FROM Exhibitions e
INNER JOIN Tickets t
    ON e.ExhibitionID = t.ExhibitionID;

SELECT
    a.FirstName || ' ' || a.LastName AS Artist,
    ar.Name AS Artifact,
    c.Name AS Category
FROM Artists a
INNER JOIN Artifacts ar
    ON a.ArtistID = ar.ArtistID
INNER JOIN Categories c
    ON ar.CategoryID = c.CategoryID;

SELECT
    v.FirstName || ' ' || v.LastName AS Visitor,
    e.Name AS Exhibition,
    t.Price
FROM Visitors v
INNER JOIN Tickets t
    ON v.VisitorID = t.VisitorID
INNER JOIN Exhibitions e
    ON t.ExhibitionID = e.ExhibitionID;

SELECT
    a.FirstName || ' ' || a.LastName AS Artist,
    ar.Name AS Artifact,
    e.Name AS Exhibition
FROM Artists a
INNER JOIN Artifacts ar
    ON a.ArtistID = ar.ArtistID
INNER JOIN ExhibitionArtifacts ea
    ON ar.ArtifactID = ea.ArtifactID
INNER JOIN Exhibitions e
    ON ea.ExhibitionID = e.ExhibitionID;

SELECT
    c.Name AS Category,
    ar.Name AS Artifact,
    e.Name AS Exhibition
FROM Categories c
INNER JOIN Artifacts ar
    ON c.CategoryID = ar.CategoryID
INNER JOIN ExhibitionArtifacts ea
    ON ar.ArtifactID = ea.ArtifactID
INNER JOIN Exhibitions e
    ON ea.ExhibitionID = e.ExhibitionID;



-- LEFT JOIN: every row of the left table is kept; columns from the right table are NULL when there is no match
SELECT
    a.FirstName,
    a.LastName,
    ar.Name AS Artifact
FROM Artists a
LEFT JOIN Artifacts ar
    ON a.ArtistID = ar.ArtistID;

-- example
SELECT
    c.Name AS Category,
    ar.Name AS Artifact
FROM Categories c
LEFT JOIN Artifacts ar
    ON c.CategoryID = ar.CategoryID;

SELECT
    e.Name AS Exhibition,
    ea.ArtifactID
FROM Exhibitions e
LEFT JOIN ExhibitionArtifacts ea
    ON e.ExhibitionID = ea.ExhibitionID;

SELECT
    ar.Name AS Artifact,
    c.Name AS Category
FROM Artifacts ar
LEFT JOIN Categories c
    ON ar.CategoryID = c.CategoryID;

SELECT
    v.FirstName,
    v.LastName,
    t.TicketID,
    t.Price
FROM Visitors v
LEFT JOIN Tickets t
    ON v.VisitorID = t.VisitorID;

SELECT
    e.Name,
    t.TicketID,
    t.Price
FROM Exhibitions e
LEFT JOIN Tickets t
    ON e.ExhibitionID = t.ExhibitionID;

SELECT
    a.FirstName || ' ' || a.LastName AS Artist,
    ar.Name AS Artifact,
    c.Name AS Category
FROM Artists a
LEFT JOIN Artifacts ar
    ON a.ArtistID = ar.ArtistID
LEFT JOIN Categories c
    ON ar.CategoryID = c.CategoryID;

SELECT
    c.Name AS Category,
    ar.Name AS Artifact,
    a.FirstName || ' ' || a.LastName AS Artist
FROM Categories c
LEFT JOIN Artifacts ar
    ON c.CategoryID = ar.CategoryID
LEFT JOIN Artists a
    ON ar.ArtistID = a.ArtistID;

SELECT
    v.FirstName || ' ' || v.LastName AS Visitor,
    t.TicketID,
    e.Name AS Exhibition
FROM Visitors v
LEFT JOIN Tickets t
    ON v.VisitorID = t.VisitorID
LEFT JOIN Exhibitions e
    ON t.ExhibitionID = e.ExhibitionID;

SELECT
    e.Name AS Exhibition,
    ea.DisplayStartDate,
    ar.Name AS Artifact
FROM Exhibitions e
LEFT JOIN ExhibitionArtifacts ea
    ON e.ExhibitionID = ea.ExhibitionID
LEFT JOIN Artifacts ar
    ON ea.ArtifactID = ar.ArtifactID;

-- RIGHT JOIN 
SELECT
    a.FirstName,
    a.LastName,
    ar.Name AS Artifact
FROM Artifacts ar
RIGHT JOIN Artists a
    ON ar.ArtistID = a.ArtistID;

-- example
SELECT
    ar.Name AS Artifact,
    c.Name AS Category
FROM Artifacts ar
RIGHT JOIN Categories c
    ON ar.CategoryID = c.CategoryID;

SELECT
    ea.ArtifactID,
    e.Name AS Exhibition
FROM ExhibitionArtifacts ea
RIGHT JOIN Exhibitions e
    ON ea.ExhibitionID = e.ExhibitionID;

SELECT
    t.TicketID,
    v.FirstName,
    v.LastName
FROM Tickets t
RIGHT JOIN Visitors v
    ON t.VisitorID = v.VisitorID;

SELECT
    t.TicketID,
    e.Name AS Exhibition,
    t.Price
FROM Tickets t
RIGHT JOIN Exhibitions e
    ON t.ExhibitionID = e.ExhibitionID;

SELECT
    ar.Name AS Artifact,
    c.Name AS Category
FROM Artifacts ar
RIGHT JOIN Categories c
    ON ar.CategoryID = c.CategoryID
WHERE c.ObjectType = 'Painting';

SELECT
    ar.Name AS Artifact,
    a.FirstName || ' ' || a.LastName AS Artist
FROM Artifacts ar
RIGHT JOIN Artists a
    ON ar.ArtistID = a.ArtistID;

SELECT
    ea.ArtifactID,
    e.Name AS Exhibition,
    ea.DisplayStartDate
FROM ExhibitionArtifacts ea
RIGHT JOIN Exhibitions e
    ON ea.ExhibitionID = e.ExhibitionID;

SELECT
    t.TicketID,
    v.Email,
    e.Name AS Exhibition
FROM Tickets t
RIGHT JOIN Visitors v
    ON t.VisitorID = v.VisitorID
LEFT JOIN Exhibitions e
    ON t.ExhibitionID = e.ExhibitionID;

SELECT
    ar.Name AS Artifact,
    c.Name AS Category,
    a.LastName AS Artist
FROM Artifacts ar
RIGHT JOIN Categories c
    ON ar.CategoryID = c.CategoryID
LEFT JOIN Artists a
    ON ar.ArtistID = a.ArtistID;

-- FULL OUTER JOIN: keeps all rows from both tables
SELECT
    a.FirstName,
    a.LastName,
    ar.Name AS Artifact
FROM Artists a
FULL OUTER JOIN Artifacts ar
    ON a.ArtistID = ar.ArtistID;

SELECT
    c.Name AS Category,
    ar.Name AS Artifact
FROM Categories c
FULL OUTER JOIN Artifacts ar
    ON c.CategoryID = ar.CategoryID;

SELECT
    e.Name AS Exhibition,
    ea.ArtifactID
FROM Exhibitions e
FULL OUTER JOIN ExhibitionArtifacts ea
    ON e.ExhibitionID = ea.ExhibitionID;

SELECT
    v.FirstName,
    v.LastName,
    t.TicketID
FROM Visitors v
FULL OUTER JOIN Tickets t
    ON v.VisitorID = t.VisitorID;

SELECT
    ar.Name AS Artifact,
    c.Name AS Category
FROM Artifacts ar
FULL OUTER JOIN Categories c
    ON ar.CategoryID = c.CategoryID;

-- SELF JOIN
SELECT
    a.FirstName || ' ' || a.LastName AS Artist,
    m.FirstName || ' ' || m.LastName AS Mentor
FROM Artists a
INNER JOIN Artists m
    ON a.MentorID = m.ArtistID;

SELECT
    a.FirstName || ' ' || a.LastName AS Artist,
    m.FirstName || ' ' || m.LastName AS Mentor
FROM Artists a
LEFT JOIN Artists m
    ON a.MentorID = m.ArtistID;

SELECT
    a.LastName AS Artist,
    m.LastName AS Mentor
FROM Artists a
INNER JOIN Artists m
    ON a.MentorID = m.ArtistID
WHERE a.MentorID IS NOT NULL;

SELECT
    a.FirstName,
    a.LastName
FROM Artists a
LEFT JOIN Artists m
    ON a.MentorID = m.ArtistID
WHERE a.MentorID IS NULL;
