PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS assessments (
    assessment_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    status TEXT NOT NULL,
    curriculum_refs_json TEXT NOT NULL,
    questions_json TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS assessment_attempts (
    attempt_id TEXT PRIMARY KEY,
    assessment_id TEXT NOT NULL,
    learner_id TEXT NOT NULL,
    status TEXT NOT NULL,
    answers_json TEXT NOT NULL,
    FOREIGN KEY (assessment_id) REFERENCES assessments(assessment_id)
        ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_assessment_attempts_learner
    ON assessment_attempts(learner_id, attempt_id);
