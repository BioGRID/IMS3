CREATE TABLE IF NOT EXISTS publication_history(
       publication_history_id      BIGINT(10)PRIMARY KEY AUTO_INCREMENT,
       modification_type           ENUM('ACTIVATED','DISABLED','DEACTIVATED','UPDATED','ANNOTATED','WRONGPROJECT','QUALITYCONTROL','ACCESSED','INPROGRESS','ABSTRACT','FULLTEXT','UNABLETOACCESS')NULL,
       publication_id              BIGINT(10)NOT NULL,
       user_id                     BIGINT(10)NOT NULL,
       publication_history_comment TEXT NULL,
       publication_history_date    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
       ,FOREIGN KEY(publication_id)REFERENCES publications(publication_id)
       ,FOREIGN KEY(user_id)REFERENCES users(user_id)
)


       