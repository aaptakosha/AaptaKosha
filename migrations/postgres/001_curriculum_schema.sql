-- PostgreSQL durable schema for AaptaKosha curriculum/catalog data.
-- Structural data is populated by the application seed pipeline; SQLite migrations remain local/dev fixtures.
CREATE TABLE IF NOT EXISTS curricula (
  curriculum_id TEXT NOT NULL, version TEXT NOT NULL,
  professional_year INTEGER NOT NULL CHECK (professional_year BETWEEN 1 AND 4),
  PRIMARY KEY (curriculum_id, version)
);
CREATE TABLE IF NOT EXISTS subjects (
  curriculum_id TEXT NOT NULL, curriculum_version TEXT NOT NULL, subject_id TEXT NOT NULL, name TEXT NOT NULL,
  PRIMARY KEY (curriculum_id, curriculum_version, subject_id),
  FOREIGN KEY (curriculum_id, curriculum_version) REFERENCES curricula(curriculum_id, version) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS curriculum_nodes (
  node_id TEXT PRIMARY KEY, curriculum_id TEXT NOT NULL, curriculum_version TEXT NOT NULL, subject_id TEXT NOT NULL,
  parent_node_id TEXT, node_type TEXT NOT NULL CHECK (node_type IN ('paper','unit','chapter','topic')), code TEXT,
  name TEXT NOT NULL, source_reference TEXT, source_locator TEXT, term INTEGER CHECK (term BETWEEN 1 AND 3),
  marks DOUBLE PRECISION, lecture_hours DOUBLE PRECISION, non_lecture_hours DOUBLE PRECISION,
  status TEXT NOT NULL DEFAULT 'structure_ready', sort_order INTEGER NOT NULL DEFAULT 0,
  FOREIGN KEY (curriculum_id,curriculum_version,subject_id) REFERENCES subjects(curriculum_id,curriculum_version,subject_id) ON DELETE CASCADE,
  FOREIGN KEY (parent_node_id) REFERENCES curriculum_nodes(node_id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_pg_curriculum_subject ON curriculum_nodes(curriculum_id,curriculum_version,subject_id,sort_order);
CREATE INDEX IF NOT EXISTS idx_pg_curriculum_parent ON curriculum_nodes(parent_node_id,sort_order);
CREATE TABLE IF NOT EXISTS classical_texts (
  text_id TEXT PRIMARY KEY, canonical_name TEXT NOT NULL, display_name TEXT NOT NULL, text_type TEXT NOT NULL,
  collection TEXT NOT NULL, description TEXT, status TEXT NOT NULL DEFAULT 'planned', sort_order INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS classical_text_professional_links (
  text_id TEXT NOT NULL REFERENCES classical_texts(text_id) ON DELETE CASCADE,
  professional_year INTEGER NOT NULL CHECK (professional_year BETWEEN 1 AND 3), PRIMARY KEY (text_id,professional_year)
);
CREATE TABLE IF NOT EXISTS classical_text_tags (
  text_id TEXT NOT NULL REFERENCES classical_texts(text_id) ON DELETE CASCADE, tag TEXT NOT NULL, PRIMARY KEY (text_id,tag)
);
