PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS content_resources (
    resource_id TEXT PRIMARY KEY,
    resource_type TEXT NOT NULL,
    title TEXT NOT NULL,
    summary TEXT NOT NULL,
    status TEXT NOT NULL,
    provenance_json TEXT NOT NULL,
    curriculum_refs_json TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS curriculum_content_links (
    curriculum_ref TEXT NOT NULL,
    resource_id TEXT NOT NULL,
    relationship TEXT NOT NULL,
    PRIMARY KEY (curriculum_ref, resource_id, relationship),
    FOREIGN KEY (resource_id) REFERENCES content_resources(resource_id)
        ON DELETE CASCADE
);
