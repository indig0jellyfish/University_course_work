-- =============================================================================
-- 02_seed.sql  |  Sample data
-- Parents first, children after, so every foreign key already has a target.
-- All people and e-mail addresses are fictional (example.com).
--
-- The data is deliberately shaped to exercise the later queries:
--   * Photography (category) and Photography Now (exhibition) have no artifacts / no tickets
--   * 'Swans Reflecting Elephants' is not shown in any exhibition
--   * 'Bird in Space' has no category (NULL)         -> LEFT / FULL OUTER JOIN demos
--   * Two visitors have no tickets, some have no phone / birth date (NULLs)
--   * Mentor links between artists are illustrative, not historical facts
-- =============================================================================

-- ---------------------------------------------------------------- Artists ----
INSERT INTO Artists (FirstName, LastName, BirthYear, Nationality) VALUES
    ('Claude',     'Monet',     1840, 'French'),
    ('Vincent',    'van Gogh',  1853, 'Dutch'),
    ('Pablo',      'Picasso',   1881, 'Spanish'),
    ('Frida',      'Kahlo',     1907, 'Mexican'),
    ('Constantin', 'Brancusi',  1876, 'Romanian'),
    ('Salvador',   'Dali',      1904, 'Spanish'),
    ('Edgar',      'Degas',     1834, 'French'),
    ('Paul',       'Cezanne',   1839, 'French'),
    ('Auguste',    'Rodin',     1840, 'French'),
    ('Georgia',    'O''Keeffe', 1887, 'American'),
    ('Ion',        'Andreescu', 1850, 'Romanian'),
    ('Gustav',     'Klimt',     1862, 'Austrian'),
    ('Anonymous',  'Medieval',  NULL, NULL);

-- Mentor relations (self-reference), looked up by name instead of hard-coded ids.
UPDATE Artists SET MentorID = (SELECT ArtistID FROM Artists WHERE LastName = 'Monet')     WHERE LastName IN ('van Gogh', 'Brancusi', 'Degas');
UPDATE Artists SET MentorID = (SELECT ArtistID FROM Artists WHERE LastName = 'van Gogh')  WHERE LastName = 'Picasso';
UPDATE Artists SET MentorID = (SELECT ArtistID FROM Artists WHERE LastName = 'Picasso')   WHERE LastName IN ('Kahlo', 'Dali');
UPDATE Artists SET MentorID = (SELECT ArtistID FROM Artists WHERE LastName = 'Degas')     WHERE LastName = 'Cezanne';

-- ------------------------------------------------------------- Categories ----
INSERT INTO Categories (Name, Description, HistoricalPeriod, ObjectType) VALUES
    ('Impressionism',      'Art based on light and visual impression.',            '19th Century', 'Painting'),
    ('Post-Impressionism', 'Style developed after Impressionism.',                 '19th Century', 'Painting'),
    ('Cubism',             'Style based on geometric forms.',                      '20th Century', 'Painting'),
    ('Surrealism',         'Movement based on imagination and the subconscious.',  '20th Century', 'Painting'),
    ('Modern Sculpture',   'Modern sculpture based on abstract forms.',            '20th Century', 'Sculpture'),
    ('Renaissance',        'European art of the Renaissance.',                     '15th Century', 'Painting'),
    ('Romanticism',        'Art centred on emotion and nature.',                   '19th Century', 'Painting'),
    ('Expressionism',      'Art based on subjective expression.',                  '20th Century', 'Painting'),
    ('Realist Sculpture',  'Sculpture with realistic forms.',                      '19th Century', 'Sculpture'),
    ('American Modernism', 'Early 20th-century American modernism.',               '20th Century', 'Painting'),
    ('Photography',        'Artistic photography.',                                '20th Century', 'Photograph');  -- no artifacts

-- ------------------------------------------------------------ Exhibitions ----
INSERT INTO Exhibitions (Name, Description, StartDate, EndDate) VALUES
    ('Light and Color',        'An exhibition about light, colour and nature.',   '2026-01-15', '2026-03-15'),
    ('European Masters',       'Works by European artists.',                      '2026-03-20', '2026-05-20'),
    ('Modern Art',             'A modern art exhibition.',                        '2026-06-01', '2026-08-20'),
    ('Women in European Art',  'An exhibition dedicated to women artists.',       '2026-09-01', '2026-11-05'),
    ('Sculpture Through Time', 'An exhibition dedicated to sculpture.',           '2026-11-01', '2027-01-15'),
    ('Renaissance Treasures',  'Treasures of the Renaissance.',                   '2025-03-01', '2025-06-30'),
    ('Expressionism Unveiled', 'An exhibition about Expressionism.',              '2025-09-10', '2025-12-10'),
    ('Impressionist Gardens',  'Gardens in Impressionist painting.',              '2026-04-01', '2026-06-15'),
    ('Romanian Heritage',      'Romanian artistic heritage.',                     '2026-10-10', '2026-12-20'),
    ('Photography Now',        'Contemporary photography.',                       '2026-12-01', '2027-02-28');  -- no artifacts, no tickets

-- --------------------------------------------------------------- Visitors ----
INSERT INTO Visitors (FirstName, LastName, Email, PhoneNumber, BirthDate) VALUES
    ('Ana',       'Popescu',   'ana.popescu@example.com',       '060000001', '2002-05-14'),
    ('Mihai',     'Rusu',      'mihai.rusu@example.com',        '060000002', '1999-08-21'),
    ('Elena',     'Ciobanu',   'elena.ciobanu@example.com',     '060000003', '2001-02-10'),
    ('Victor',    'Moraru',    'victor.moraru@example.com',     '060000004', '1998-11-30'),
    ('Maria',     'Ceban',     'maria.ceban@example.com',       '060000005', '2003-07-07'),
    ('Ion',       'Munteanu',  'ion.munteanu@example.com',      '060000006', '1985-03-12'),
    ('Cristina',  'Lungu',     'cristina.lungu@example.com',    '060000007', '1995-09-25'),
    ('Andrei',    'Bostan',    'andrei.bostan@example.com',     '060000008', '1978-12-01'),
    ('Natalia',   'Gutu',      'natalia.gutu@example.com',      NULL,        '1990-06-18'),
    ('Dumitru',   'Sandu',     'dumitru.sandu@example.com',     '060000010', NULL),
    ('Olga',      'Railean',   'olga.railean@example.com',      '060000011', '1967-01-30'),
    ('Serghei',   'Popa',      'serghei.popa@example.com',      '060000012', '2005-04-09'),
    ('Irina',     'Vrabie',    'irina.vrabie@example.com',      '060000013', '2000-10-22'),
    ('Alexandru', 'Cojocaru',  'alexandru.cojocaru@example.com','060000014', '1992-07-14'),
    ('Diana',     'Lupu',      'diana.lupu@example.com',        '060000015', '2008-02-27'),   -- no tickets
    ('Radu',      'Turcanu',   'radu.turcanu@example.com',      '060000016', '1988-11-05'),
    ('Tatiana',   'Botnaru',   'tatiana.botnaru@example.com',   NULL,        '1973-08-19');   -- no tickets

-- -------------------------------------------------------------- Artifacts ----
-- First batch: ids are explicit through the column list; 'Bird in Space' has no category.
INSERT INTO Artifacts (Name, Description, CreationYear, ArtistID, CategoryID) VALUES
    ('Water Lilies',  'Painting of water lilies.',                       1906, 1, 1),
    ('Starry Night',  'One of the artist''s best-known works.',          1889, 2, 2),
    ('Guernica',      'Monumental painting on the theme of war.',        1937, 3, 3),
    ('Self Portrait', 'Self-portrait of the artist.',                    1940, 4, 4),
    ('Bird in Space', 'Abstract modern sculpture.',                      1928, 5, NULL);

-- Second batch: artist and category are resolved by name, so no ids are hard-coded.
INSERT INTO Artifacts (Name, Description, CreationYear, ArtistID, CategoryID)
SELECT d.name, d.descr, d.yr, ar.ArtistID, c.CategoryID
FROM (VALUES
    ('Impression, Sunrise',        'The painting that gave Impressionism its name.', 1872, 'Monet',     'Impressionism'),
    ('Haystacks',                  'Series of paintings of haystacks.',              1890, 'Monet',     'Impressionism'),
    ('Sunflowers',                 'Still life with sunflowers.',                    1888, 'van Gogh',  'Post-Impressionism'),
    ('The Bedroom',                'Painting of the bedroom in Arles.',              1888, 'van Gogh',  'Post-Impressionism'),
    ('The Dance Class',            'Ballerinas in a rehearsal room.',                1874, 'Degas',     'Impressionism'),
    ('Mont Sainte-Victoire',       'Landscape with the mountain in Provence.',       1904, 'Cezanne',   'Post-Impressionism'),
    ('The Card Players',           NULL,                                             1894, 'Cezanne',   'Post-Impressionism'),
    ('The Persistence of Memory',  'Melting clocks in a dreamlike landscape.',       1931, 'Dali',      'Surrealism'),
    ('Swans Reflecting Elephants', NULL,                                             1937, 'Dali',      'Surrealism'),
    ('Les Demoiselles d''Avignon', 'Early work of Cubism.',                          1907, 'Picasso',   'Cubism'),
    ('The Old Guitarist',          'From the Blue Period.',                          1904, 'Picasso',   'Expressionism'),
    ('The Two Fridas',             'Double self-portrait.',                          1939, 'Kahlo',     'Surrealism'),
    ('The Broken Column',          'Self-portrait about pain.',                      1944, 'Kahlo',     'Surrealism'),
    ('The Thinker',                'Bronze sculpture.',                              1904, 'Rodin',     'Realist Sculpture'),
    ('The Kiss',                   'Marble sculpture.',                              1882, 'Rodin',     'Realist Sculpture'),
    ('The Endless Column',         'The column without end.',                        1938, 'Brancusi',  'Modern Sculpture'),
    ('Sleeping Muse',              'Oval bronze head.',                              1910, 'Brancusi',  'Modern Sculpture'),
    ('Black Iris',                 'Close-up of a flower.',                          1926, 'O''Keeffe', 'American Modernism'),
    ('Winter Landscape',           'Winter landscape.',                              1880, 'Andreescu', 'Romanticism'),
    ('Medieval Icon',              'Icon painted on wood.',                          NULL, 'Medieval',  'Renaissance')
) AS d(name, descr, yr, lastname, catname)
JOIN Artists    ar ON ar.LastName = d.lastname
JOIN Categories c  ON c.Name      = d.catname
ORDER BY d.yr NULLS LAST, d.name;

-- -------------------------------------------------- ExhibitionArtifacts ----
INSERT INTO ExhibitionArtifacts (ExhibitionID, ArtifactID, DisplayStartDate, DisplayEndDate)
SELECT e.ExhibitionID, a.ArtifactID, d.ds::date, d.de::date
FROM (VALUES
    ('Light and Color',        'Water Lilies',               '2026-01-15', '2026-03-15'),
    ('European Masters',       'Starry Night',               '2026-03-20', '2026-05-20'),
    ('Modern Art',             'Guernica',                   '2026-06-01', '2026-08-15'),
    ('Women in European Art',  'Self Portrait',              '2026-09-01', '2026-10-31'),
    ('Sculpture Through Time', 'Bird in Space',              '2026-11-01', '2027-01-15'),
    ('Light and Color',        'Impression, Sunrise',        '2026-01-15', '2026-03-15'),
    ('Light and Color',        'Haystacks',                  '2026-01-15', '2026-03-15'),
    ('Light and Color',        'The Dance Class',            '2026-01-20', '2026-03-10'),
    ('Impressionist Gardens',  'Haystacks',                  '2026-04-01', '2026-06-15'),
    ('Impressionist Gardens',  'Sunflowers',                 '2026-04-01', '2026-06-15'),
    ('Impressionist Gardens',  'The Dance Class',            '2026-04-05', '2026-06-10'),
    ('European Masters',       'Mont Sainte-Victoire',       '2026-03-20', '2026-05-20'),
    ('European Masters',       'The Card Players',           '2026-03-20', '2026-05-20'),
    ('European Masters',       'Les Demoiselles d''Avignon', '2026-03-25', '2026-05-15'),
    ('European Masters',       'Sunflowers',                 '2026-03-20', '2026-03-31'),
    ('Modern Art',             'The Persistence of Memory',  '2026-06-01', '2026-08-20'),
    ('Modern Art',             'Les Demoiselles d''Avignon', '2026-06-01', '2026-08-20'),
    ('Modern Art',             'Black Iris',                 '2026-06-10', '2026-08-15'),
    ('Women in European Art',  'The Two Fridas',             '2026-09-01', '2026-11-05'),
    ('Women in European Art',  'The Broken Column',          '2026-09-01', '2026-11-05'),
    ('Women in European Art',  'Black Iris',                 '2026-09-05', '2026-10-31'),
    ('Sculpture Through Time', 'The Thinker',                '2026-11-01', '2027-01-15'),
    ('Sculpture Through Time', 'The Kiss',                   '2026-11-01', '2027-01-15'),
    ('Sculpture Through Time', 'The Endless Column',         '2026-11-05', '2027-01-10'),
    ('Sculpture Through Time', 'Sleeping Muse',              '2026-11-05', '2027-01-10'),
    ('Renaissance Treasures',  'Medieval Icon',              '2025-03-01', '2025-06-30'),
    ('Expressionism Unveiled', 'The Old Guitarist',          '2025-09-10', '2025-12-10'),
    ('Expressionism Unveiled', 'The Bedroom',                '2025-09-15', '2025-12-05'),
    ('Romanian Heritage',      'Winter Landscape',           '2026-10-10', '2026-12-20'),
    ('Romanian Heritage',      'The Endless Column',         '2026-10-10', '2026-10-31'),
    ('Romanian Heritage',      'Sleeping Muse',              '2026-10-10', '2026-10-31')
) AS d(exname, artname, ds, de)
JOIN Exhibitions e ON e.Name = d.exname
JOIN Artifacts   a ON a.Name = d.artname
ORDER BY e.ExhibitionID, a.ArtifactID;

-- ---------------------------------------------------------------- Tickets ----
-- Past exhibitions mostly have used tickets; upcoming ones have unused tickets.
INSERT INTO Tickets (VisitorID, ExhibitionID, PurchaseDate, VisitDate, Price, IsUsed)
SELECT v.VisitorID, e.ExhibitionID, d.pd::date, d.vd::date, d.price, d.used
FROM (VALUES
    -- Renaissance Treasures
    ('ion.munteanu@example.com',       'Renaissance Treasures',  '2025-03-02', '2025-03-10',  80.00, TRUE),
    ('cristina.lungu@example.com',     'Renaissance Treasures',  '2025-04-01', '2025-04-15',  80.00, TRUE),
    ('andrei.bostan@example.com',      'Renaissance Treasures',  '2025-05-10', '2025-05-20',  95.00, TRUE),
    -- Expressionism Unveiled
    ('ion.munteanu@example.com',       'Expressionism Unveiled', '2025-09-01', '2025-09-20',  90.00, TRUE),
    ('olga.railean@example.com',       'Expressionism Unveiled', '2025-10-05', '2025-10-15',  90.00, TRUE),
    ('natalia.gutu@example.com',       'Expressionism Unveiled', '2025-11-01', '2025-11-12', 110.00, TRUE),
    ('serghei.popa@example.com',       'Expressionism Unveiled', '2025-11-20', '2025-12-01',  75.00, TRUE),
    -- Light and Color
    ('ana.popescu@example.com',        'Light and Color',        '2026-01-10', '2026-02-01', 100.00, TRUE),
    ('ana.popescu@example.com',        'Light and Color',        '2026-01-20', '2026-02-10', 100.00, TRUE),
    ('cristina.lungu@example.com',     'Light and Color',        '2026-01-25', '2026-02-15', 100.00, TRUE),
    ('mihai.rusu@example.com',         'Light and Color',        '2026-02-01', '2026-02-20', 115.00, TRUE),
    ('irina.vrabie@example.com',       'Light and Color',        '2026-02-10', '2026-03-01',  95.00, TRUE),
    ('ion.munteanu@example.com',       'Light and Color',        '2026-02-20', '2026-03-05', 100.00, TRUE),
    -- European Masters
    ('mihai.rusu@example.com',         'European Masters',       '2026-03-01', '2026-04-10', 120.00, TRUE),
    ('elena.ciobanu@example.com',      'European Masters',       '2026-03-25', '2026-04-10', 130.00, TRUE),
    ('andrei.bostan@example.com',      'European Masters',       '2026-04-02', '2026-04-18', 125.00, TRUE),
    ('victor.moraru@example.com',      'European Masters',       '2026-04-20', '2026-05-05', 140.00, TRUE),
    ('alexandru.cojocaru@example.com', 'European Masters',       '2026-04-25', '2026-05-10', 120.00, TRUE),
    ('olga.railean@example.com',       'European Masters',       '2026-05-01', '2026-05-15', 135.00, TRUE),
    -- Impressionist Gardens
    ('maria.ceban@example.com',        'Impressionist Gardens',  '2026-04-05', '2026-04-22',  85.00, TRUE),
    ('irina.vrabie@example.com',       'Impressionist Gardens',  '2026-05-02', '2026-05-20',  85.00, TRUE),
    ('radu.turcanu@example.com',       'Impressionist Gardens',  '2026-05-20', '2026-06-05',  90.00, TRUE),
    ('ana.popescu@example.com',        'Impressionist Gardens',  '2026-05-25', '2026-06-10',  85.00, TRUE),
    -- Modern Art
    ('elena.ciobanu@example.com',      'Modern Art',             '2026-05-20', '2026-07-10', 150.00, FALSE),
    ('mihai.rusu@example.com',         'Modern Art',             '2026-06-05', '2026-06-20', 150.00, TRUE),
    ('serghei.popa@example.com',       'Modern Art',             '2026-06-18', '2026-07-02', 160.00, TRUE),
    ('cristina.lungu@example.com',     'Modern Art',             '2026-07-01', '2026-07-15', 155.00, TRUE),
    ('alexandru.cojocaru@example.com', 'Modern Art',             '2026-07-20', '2026-08-05', 150.00, FALSE),
    ('victor.moraru@example.com',      'Modern Art',             '2026-07-25', '2026-08-10', 170.00, TRUE),
    -- Women in European Art
    ('victor.moraru@example.com',      'Women in European Art',  '2026-08-20', '2026-09-15', 130.00, FALSE),
    ('natalia.gutu@example.com',       'Women in European Art',  '2026-08-25', '2026-09-10', 120.00, TRUE),
    ('maria.ceban@example.com',        'Women in European Art',  '2026-09-05', '2026-09-20', 120.00, TRUE),
    ('ana.popescu@example.com',        'Women in European Art',  '2026-09-15', '2026-10-01', 125.00, TRUE),
    ('irina.vrabie@example.com',       'Women in European Art',  '2026-10-02', '2026-10-18', 120.00, TRUE),
    ('olga.railean@example.com',       'Women in European Art',  '2026-10-15', '2026-10-30', 130.00, FALSE),
    ('radu.turcanu@example.com',       'Women in European Art',  '2026-10-18', '2026-11-02', 130.00, FALSE),
    ('elena.ciobanu@example.com',      'Women in European Art',  '2026-10-19', '2026-11-03', 125.00, FALSE),
    -- Romanian Heritage
    ('ion.munteanu@example.com',       'Romanian Heritage',      '2026-10-12', '2026-10-25',  70.00, FALSE),
    ('andrei.bostan@example.com',      'Romanian Heritage',      '2026-10-15', '2026-11-08',  70.00, FALSE),
    ('dumitru.sandu@example.com',      'Romanian Heritage',      '2026-10-20', '2026-10-24',  70.00, FALSE),
    ('cristina.lungu@example.com',     'Romanian Heritage',      '2026-10-20', '2026-12-05',  75.00, FALSE),
    -- Sculpture Through Time
    ('maria.ceban@example.com',        'Sculpture Through Time', '2026-10-01', '2026-11-15', 110.00, FALSE),
    ('victor.moraru@example.com',      'Sculpture Through Time', '2026-10-10', '2026-11-10', 140.00, FALSE),
    ('mihai.rusu@example.com',         'Sculpture Through Time', '2026-10-12', '2026-11-20', 140.00, FALSE),
    ('ana.popescu@example.com',        'Sculpture Through Time', '2026-10-18', '2026-12-01', 145.00, FALSE),
    ('maria.ceban@example.com',        'Sculpture Through Time', '2026-10-20', '2027-01-05', 140.00, FALSE)
) AS d(email, exname, pd, vd, price, used)
JOIN Visitors    v ON v.Email = d.email
JOIN Exhibitions e ON e.Name  = d.exname
ORDER BY d.pd, d.email;
