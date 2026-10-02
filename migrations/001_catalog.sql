PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS curricula (
    curriculum_id TEXT NOT NULL,
    version TEXT NOT NULL,
    professional_year INTEGER NOT NULL CHECK (professional_year >= 1),
    PRIMARY KEY (curriculum_id, version)
);

CREATE TABLE IF NOT EXISTS subjects (
    curriculum_id TEXT NOT NULL,
    curriculum_version TEXT NOT NULL,
    subject_id TEXT NOT NULL,
    name TEXT NOT NULL,
    PRIMARY KEY (curriculum_id, curriculum_version, subject_id),
    FOREIGN KEY (curriculum_id, curriculum_version)
        REFERENCES curricula(curriculum_id, version)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS topics (
    curriculum_id TEXT NOT NULL,
    curriculum_version TEXT NOT NULL,
    subject_id TEXT NOT NULL,
    topic_id TEXT NOT NULL,
    name TEXT NOT NULL,
    PRIMARY KEY (curriculum_id, curriculum_version, subject_id, topic_id),
    FOREIGN KEY (curriculum_id, curriculum_version, subject_id)
        REFERENCES subjects(curriculum_id, curriculum_version, subject_id)
        ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_subjects_curriculum
    ON subjects(curriculum_id, curriculum_version);

CREATE INDEX IF NOT EXISTS idx_topics_subject
    ON topics(curriculum_id, curriculum_version, subject_id);
