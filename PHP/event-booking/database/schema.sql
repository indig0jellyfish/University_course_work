-- Lucrarea de laborator nr. 5 - Mini-sistem de rezervari evenimente
-- Import in HeidiSQL (Laragon): File > Run SQL file...  (MySQL 8.0.16+ / MariaDB 10.2.1+, InnoDB)

CREATE DATABASE IF NOT EXISTS event_booking CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE event_booking;

DROP TABLE IF EXISTS reservations;
DROP TABLE IF EXISTS events;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
  id            INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  username      VARCHAR(30)  NOT NULL,
  email         VARCHAR(190) NOT NULL,
  password_hash VARCHAR(255) NOT NULL,              -- rezultatul password_hash() (bcrypt)
  created_at    TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY uq_users_username (username),
  UNIQUE KEY uq_users_email (email)
) ENGINE=InnoDB;

-- 1 user -> N events
CREATE TABLE events (
  id             INT UNSIGNED      NOT NULL AUTO_INCREMENT PRIMARY KEY,
  owner_id       INT UNSIGNED      NOT NULL,
  title          VARCHAR(120)      NOT NULL,
  description    TEXT              NOT NULL,
  location       VARCHAR(150)      NOT NULL,
  start_datetime DATETIME          NOT NULL,
  capacity       SMALLINT UNSIGNED NOT NULL,
  created_at     TIMESTAMP         NOT NULL DEFAULT CURRENT_TIMESTAMP,
  KEY idx_events_owner (owner_id, created_at),      -- "evenimentele mele", sortate dupa data adaugarii
  FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE,
  CHECK (capacity BETWEEN 1 AND 500)
) ENGINE=InnoDB;

-- users <-> events este N:M, rezolvata prin reservations
CREATE TABLE reservations (
  id         INT UNSIGNED      NOT NULL AUTO_INCREMENT PRIMARY KEY,
  event_id   INT UNSIGNED      NOT NULL,
  user_id    INT UNSIGNED      NOT NULL,
  seats      SMALLINT UNSIGNED NOT NULL,
  notes      VARCHAR(500)      NULL,
  created_at TIMESTAMP         NOT NULL DEFAULT CURRENT_TIMESTAMP,
  KEY idx_res_event (event_id),                     -- SUM(seats) per eveniment
  KEY idx_res_user (user_id),                       -- "rezervarile mele"
  FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
  FOREIGN KEY (user_id)  REFERENCES users(id)  ON DELETE CASCADE,
  CHECK (seats >= 1)
) ENGINE=InnoDB;
