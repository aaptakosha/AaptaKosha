PRAGMA foreign_keys = ON;

-- AaptaKosha BAMS structural catalogue.
-- Detailed topics/content are intentionally populated in a later content-ingestion phase.

INSERT OR IGNORE INTO curricula (curriculum_id, version, professional_year) VALUES
  ('bams_ncism_1', '2021-22', 1),
  ('bams_ncism_2', '2021-22', 2),
  ('bams_ncism_3', '2021-22', 3);

INSERT OR IGNORE INTO subjects (curriculum_id, curriculum_version, subject_id, name) VALUES
  ('bams_ncism_1', '2021-22', 'AyUG-SN-AI', 'Sanskrit evam Ayurved Itihas'),
  ('bams_ncism_1', '2021-22', 'AyUG-PV', 'Padartha Vijnanam'),
  ('bams_ncism_1', '2021-22', 'AyUG-SA1', 'Samhita Adhyayan-1'),
  ('bams_ncism_1', '2021-22', 'AyUG-RS', 'Rachana Sharira'),
  ('bams_ncism_1', '2021-22', 'AyUG-KS', 'Kriya Sharira'),
  ('bams_ncism_2', '2021-22', 'AyUG-RB', 'Rasashastra evam Bhaishajyakalpana'),
  ('bams_ncism_2', '2021-22', 'AyUG-AT', 'Agada Tantra evam Vidhi Vaidyaka'),
  ('bams_ncism_2', '2021-22', 'AyUG-SA2', 'Samhita Adhyayan-2'),
  ('bams_ncism_2', '2021-22', 'AyUG-DG', 'Dravyaguna Vijnana'),
  ('bams_ncism_2', '2021-22', 'AyUG-RN', 'Roga Nidan evam Vikriti Vijnana'),
  ('bams_ncism_2', '2021-22', 'AyUG-SW', 'Swasthavritta evam Yoga'),
  ('bams_ncism_3', '2021-22', 'AyUG-KC', 'Kayachikitsa'),
  ('bams_ncism_3', '2021-22', 'AyUG-PK', 'Panchakarma & Upakarma'),
  ('bams_ncism_3', '2021-22', 'AyUG-ST', 'Shalya Tantra'),
  ('bams_ncism_3', '2021-22', 'AyUG-SL', 'Shalakya Tantra'),
  ('bams_ncism_3', '2021-22', 'AyUG-PS', 'Prasuti Tantra evam Stree Roga'),
  ('bams_ncism_3', '2021-22', 'AyUG-KB', 'Kaumarabhritya'),
  ('bams_ncism_3', '2021-22', 'AyUG-SA3', 'Samhita Adhyayan-3'),
  ('bams_ncism_3', '2021-22', 'AyUG-EM', 'Atyaikachikitsa / Emergency Medicine'),
  ('bams_ncism_3', '2021-22', 'AyUG-RM', 'Research Methodology and Medical Statistics');

CREATE TABLE IF NOT EXISTS classical_texts (
    text_id TEXT PRIMARY KEY, canonical_name TEXT NOT NULL, display_name TEXT NOT NULL,
    text_type TEXT NOT NULL, collection TEXT NOT NULL, description TEXT,
    status TEXT NOT NULL DEFAULT 'planned', sort_order INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS classical_text_professional_links (
    text_id TEXT NOT NULL, professional_year INTEGER NOT NULL CHECK (professional_year BETWEEN 1 AND 3),
    PRIMARY KEY (text_id, professional_year),
    FOREIGN KEY (text_id) REFERENCES classical_texts(text_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS classical_text_tags (
    text_id TEXT NOT NULL, tag TEXT NOT NULL, PRIMARY KEY (text_id, tag),
    FOREIGN KEY (text_id) REFERENCES classical_texts(text_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_classical_text_collection ON classical_texts(collection, sort_order);
CREATE INDEX IF NOT EXISTS idx_classical_text_professional ON classical_text_professional_links(professional_year);

INSERT OR IGNORE INTO classical_texts (text_id, canonical_name, display_name, text_type, collection, description, sort_order) VALUES
('charaka-samhita','Charaka Samhita','Charaka Samhita','samhita','brihattrayi','Major classical Ayurvedic text; central to NCISM Samhita Adhyayan. ',10),
('sushruta-samhita','Sushruta Samhita','Sushruta Samhita','samhita','brihattrayi','Major classical Ayurvedic text with strong shalya and sharira relevance.',20),
('ashtanga-hridaya','Ashtanga Hridaya','Ashtanga Hridaya','samhita','brihattrayi','Major classical Ayurvedic compendium used extensively across BAMS study.',30),
('ashtanga-sangraha','Ashtanga Sangraha','Ashtanga Sangraha','samhita','other_major_classical','Major classical compendium closely related to the Ashtanga tradition.',40),
('kashyapa-samhita','Kashyapa Samhita','Kashyapa Samhita','samhita','other_major_classical','Classical text of special relevance to Kaumarabhritya and related subjects.',50),
('bhela-samhita','Bhela Samhita','Bhela Samhita','samhita','other_major_classical','Early classical Ayurvedic text preserved in manuscript tradition.',60),
('harita-samhita','Harita Samhita','Harita Samhita','samhita','other_major_classical','Classical Ayurvedic text included for extended textual discovery.',70),
('madhava-nidana','Madhava Nidana','Madhava Nidana','samhita','laghutrayi','Important diagnostic compendium traditionally grouped among Laghutrayi.',80),
('sharangadhara-samhita','Sharangadhara Samhita','Sharangadhara Samhita','samhita','laghutrayi','Important later Ayurvedic compendium traditionally grouped among Laghutrayi.',90),
('bhavaprakasha','Bhavaprakasha','Bhavaprakasha','samhita','laghutrayi','Important later Ayurvedic compendium traditionally grouped among Laghutrayi.',100),
('chakradatta','Chakradatta','Chakradatta','compendium','later_compendia','Important therapeutic compendium; not labelled as Brihattrayi/Laghutrayi.',110),
('yogaratnakara','Yogaratnakara','Yogaratnakara','compendium','later_compendia','Later therapeutic compendium.',120),
('bhaishajya-ratnavali','Bhaishajya Ratnavali','Bhaishajya Ratnavali','compendium','later_compendia','Important later formulary/therapeutic compendium.',130),
('gadanigraha','Gadanigraha','Gadanigraha','compendium','later_compendia','Later Ayurvedic therapeutic compendium.',140),
('vangasena-samhita','Vangasena Samhita','Vangasena Samhita','samhita','later_compendia','Later Ayurvedic compendium.',150),
('bhavaprakasha-nighantu','Bhavaprakasha Nighantu','Bhavaprakasha Nighantu','nighantu','nighantu','Materia-medica reference; kept separate from Samhita classifications.',160),
('dhanvantari-nighantu','Dhanvantari Nighantu','Dhanvantari Nighantu','nighantu','nighantu','Classical materia-medica reference.',170),
('raja-nighantu','Raja Nighantu','Raja Nighantu','nighantu','nighantu','Classical materia-medica reference.',180),
('kaiyadeva-nighantu','Kaiyadeva Nighantu','Kaiyadeva Nighantu','nighantu','nighantu','Classical materia-medica reference.',190),
('madanapala-nighantu','Madanapala Nighantu','Madanapala Nighantu','nighantu','nighantu','Classical materia-medica reference.',200);

INSERT OR IGNORE INTO classical_text_professional_links (text_id, professional_year) VALUES
('charaka-samhita',1),('charaka-samhita',2),('charaka-samhita',3),
('sushruta-samhita',1),('sushruta-samhita',2),('sushruta-samhita',3),
('ashtanga-hridaya',1),('ashtanga-hridaya',2),('ashtanga-hridaya',3),
('ashtanga-sangraha',1),('kashyapa-samhita',3),('bhela-samhita',1),('harita-samhita',1),
('madhava-nidana',2),('madhava-nidana',3),('sharangadhara-samhita',2),('sharangadhara-samhita',3),
('bhavaprakasha',2),('bhavaprakasha',3),('chakradatta',2),('chakradatta',3),
('yogaratnakara',2),('yogaratnakara',3),('bhaishajya-ratnavali',2),('bhaishajya-ratnavali',3),
('gadanigraha',2),('gadanigraha',3),('vangasena-samhita',2),('vangasena-samhita',3),
('bhavaprakasha-nighantu',2),('dhanvantari-nighantu',2),('raja-nighantu',2),
('kaiyadeva-nighantu',2),('madanapala-nighantu',2);

INSERT OR IGNORE INTO classical_text_tags (text_id, tag)
SELECT text_id, 'aiapget' FROM classical_texts
WHERE text_id IN ('charaka-samhita','sushruta-samhita','ashtanga-hridaya','ashtanga-sangraha','kashyapa-samhita','madhava-nidana','sharangadhara-samhita','bhavaprakasha');