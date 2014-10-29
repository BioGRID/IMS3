-- table described in the comment of the docs, not in the docs itself.
CREATE TABLE IF NOT EXISTS participant_types(
       participant_type_id	  BIGINT(10)PRIMARY KEY AUTO_INCREMENT,
       participant_type_name	  VARCHAR(255)UNIQUE,
       participant_type_status	  ENUM('active','inactive')NOT NULL DEFAULT 'active',
       participant_type_addeddate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO participant_types(participant_type_name)VALUES('Gene');

CREATE TABLE IF NOT EXISTS participants(
       participant_id	     BIGINT(10)PRIMARY KEY AUTO_INCREMENT,
       participant_value     BIGINT(10)NOT NULL, -- phony foreign key
       participant_type_id   BIGINT(10)NULL, -- null meant unknow participant
       participant_addeddate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
       participant_status    ENUM('active','inactive')NOT NULL DEFAULT 'active',
       FOREIGN KEY(participant_type_id)REFERENCES participant_types(participant_type_id),
       UNIQUE KEY(participant_value,participant_type_id)
);

CREATE TABLE IF NOT EXISTS participant_roles(
       participant_role_id        BIGINT(10)PRIMARY KEY AUTO_INCREMENT,
       participant_role_name	  VARCHAR(255)UNIQUE,
       participant_role_addeddate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
       participant_role_status	  ENUM('active','inactive')NOT NULL DEFAULT 'active'
);

-- These are refereed to by participant_role_id in the
-- Interaction_type.js file.  If they change this changes too.
INSERT INTO participant_roles(participant_role_id,participant_role_name)VALUES
       (1,'unspecified'),
       (2,'bait'),(3,'hit');
--       ('ancillary'),('suppressor'),('suppressed'),
