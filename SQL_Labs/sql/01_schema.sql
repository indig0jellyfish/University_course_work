-- =============================================================================
-- 01_schema.sql  |  Museum database (PostgreSQL)
-- Tables, keys, referential actions and integrity constraints.
-- Re-runnable: drops everything it creates first.
--
-- Note: identifiers are unquoted, so PostgreSQL stores them in lower case
-- (Artists -> artists, ArtistID -> artistid). Queries work in either spelling.
-- =============================================================================

SET client_min_messages = warning;   -- hide "does not exist, skipping" notices

DROP VIEW  IF EXISTS v_exhibitions_above_average, v_top5_tickets, v_active_tickets,
                     v_artifact_details, v_exhibition_revenue;
DROP TABLE IF EXISTS tickets_test;
DROP TABLE IF EXISTS Tickets, ExhibitionArtifacts, Artifacts, Visitors,
                     Exhibitions, Categories, Artists CASCADE;


CREATE TABLE Artists (
    ArtistID    SERIAL PRIMARY KEY,
    FirstName   VARCHAR(50) NOT NULL,
    LastName    VARCHAR(50) NOT NULL,
    BirthYear   INT CHECK (BirthYear > 0),
    Nationality VARCHAR(50),
    -- Self-reference used for the SELF JOIN demo (artist -> mentor).
    -- Default referential action (NO ACTION): an artist who is someone's mentor cannot be deleted.
    MentorID    INT REFERENCES Artists(ArtistID)
);

CREATE TABLE Categories (
    CategoryID       SERIAL PRIMARY KEY,
    Name             VARCHAR(100) NOT NULL,
    Description      TEXT,
    HistoricalPeriod VARCHAR(100),
    ObjectType       VARCHAR(100)
);

CREATE TABLE Exhibitions (
    ExhibitionID SERIAL PRIMARY KEY,
    Name         VARCHAR(100) NOT NULL,
    Description  TEXT,
    StartDate    DATE NOT NULL,
    EndDate      DATE NOT NULL,

    CHECK (EndDate >= StartDate)
);

CREATE TABLE Artifacts (
    ArtifactID   SERIAL PRIMARY KEY,
    Name         VARCHAR(100) NOT NULL,
    Description  TEXT,
    CreationYear INT CHECK (CreationYear > 0),
    ArtistID     INT NOT NULL,
    -- Nullable on purpose: an artifact may be catalogued before it is categorised.
    -- This is what makes the LEFT / RIGHT / FULL OUTER JOIN demos meaningful.
    CategoryID   INT,

    -- RESTRICT: an artist or category cannot be deleted while artifacts still reference it.
    FOREIGN KEY (ArtistID)
        REFERENCES Artists(ArtistID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    FOREIGN KEY (CategoryID)
        REFERENCES Categories(CategoryID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- Junction table for the many-to-many relation Exhibitions <-> Artifacts.
CREATE TABLE ExhibitionArtifacts (
    ExhibitionArtifactID SERIAL PRIMARY KEY,
    ExhibitionID         INT NOT NULL,
    ArtifactID           INT NOT NULL,
    DisplayStartDate     DATE NOT NULL,
    DisplayEndDate       DATE NOT NULL,

    CHECK (DisplayEndDate >= DisplayStartDate),

    -- CASCADE: the link rows are meaningless without either parent, so they go with it.
    FOREIGN KEY (ExhibitionID)
        REFERENCES Exhibitions(ExhibitionID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    FOREIGN KEY (ArtifactID)
        REFERENCES Artifacts(ArtifactID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    -- The same artifact cannot be listed twice in the same exhibition.
    UNIQUE (ExhibitionID, ArtifactID)
);

CREATE TABLE Visitors (
    VisitorID   SERIAL PRIMARY KEY,
    FirstName   VARCHAR(50)  NOT NULL,
    LastName    VARCHAR(50)  NOT NULL,
    Email       VARCHAR(100) NOT NULL UNIQUE,
    PhoneNumber VARCHAR(20),
    BirthDate   DATE
);

CREATE TABLE Tickets (
    TicketID     SERIAL PRIMARY KEY,
    VisitorID    INT NOT NULL,
    ExhibitionID INT NOT NULL,
    PurchaseDate DATE NOT NULL DEFAULT CURRENT_DATE,
    VisitDate    DATE NOT NULL,
    Price        DECIMAL(10,2) NOT NULL CHECK (Price > 0),
    IsUsed       BOOLEAN NOT NULL DEFAULT FALSE,

    -- RESTRICT: sold tickets are financial records, so visitors/exhibitions with tickets cannot be deleted.
    FOREIGN KEY (VisitorID)
        REFERENCES Visitors(VisitorID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    FOREIGN KEY (ExhibitionID)
        REFERENCES Exhibitions(ExhibitionID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);
