CREATE TABLE IF NOT EXISTS publications(
       publication_id		 BIGINT(10) PRIMARY KEY AUTO_INCREMENT,
       publication_pubmed_id	 BIGINT(10) NOT NULL UNIQUE,
       publication_article_title TEXT NULL,
       publication_abstract	 MEDIUMTEXT NULL,
       publication_author_short	 VARCHAR(255) NULL,
       publication_author_full	 TEXT NULL,
       publication_volumne	 BIGINT(10) NULL,
       publication_issue	 BIGINT(10) NULL,
       publication_date		 DATE NULL,
       publication_journal	 VARCHAR(255) NULL,
       publication_pagination	 VARCHAR(255) NULL,
       publication_affiliation	 TEXT NULL,
       publication_meshterms	 TEXT NULL,
       publication_status	 ENUM('active','inactive')NOT NULL DEFAULT 'active',
       publication_addeddate	 TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
       publication_lastupdated	 TIMESTAMP NULL
);

CREATE TABLE IF NOT EXISTS publication_notes(
       publication_note_id        BIGINT(10) PRIMARY KEY AUTO_INCREMENT,
       publication_note_text      TEXT NOT NULL,
       user_id			  BIGINT(10) NOT NULL,
       publication_node_addeddate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
       publication_note_status	  ENUM('active','inactive'),
       publication_id		  BIGINT(10) NOT NULL,
       FOREIGN KEY(user_id)REFERENCES users(user_id),
       FOREIGN KEY(publication_id)REFERENCES publications(publication_id)
);