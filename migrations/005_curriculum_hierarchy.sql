PRAGMA foreign_keys = ON;

-- Hierarchical NCISM curriculum nodes.
-- One node can be a paper, unit, chapter, or topic; parent_node_id preserves the tree.
CREATE TABLE IF NOT EXISTS curriculum_nodes (
    node_id TEXT PRIMARY KEY,
    curriculum_id TEXT NOT NULL,
    curriculum_version TEXT NOT NULL,
    subject_id TEXT NOT NULL,
    parent_node_id TEXT,
    node_type TEXT NOT NULL CHECK (node_type IN ('paper','unit','chapter','topic')),
    code TEXT,
    name TEXT NOT NULL,
    source_reference TEXT,
    source_locator TEXT,
    term INTEGER CHECK (term BETWEEN 1 AND 3),
    marks REAL,
    lecture_hours REAL,
    non_lecture_hours REAL,
    status TEXT NOT NULL DEFAULT 'structure_ready'
        CHECK (status IN ('planned','structure_ready','content_in_progress','review','published')),
    sort_order INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (curriculum_id, curriculum_version, subject_id)
        REFERENCES subjects(curriculum_id, curriculum_version, subject_id)
        ON DELETE CASCADE,
    FOREIGN KEY (parent_node_id) REFERENCES curriculum_nodes(node_id)
        ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_curriculum_nodes_subject
    ON curriculum_nodes(curriculum_id, curriculum_version, subject_id, sort_order);

CREATE INDEX IF NOT EXISTS idx_curriculum_nodes_parent
    ON curriculum_nodes(parent_node_id, sort_order);

CREATE INDEX IF NOT EXISTS idx_curriculum_nodes_type
    ON curriculum_nodes(node_type);

-- Initial source-verified nodes. These are structural anchors only; detailed teaching
-- content is deliberately not stored in this migration.
INSERT OR IGNORE INTO curriculum_nodes
(node_id,curriculum_id,curriculum_version,subject_id,parent_node_id,node_type,code,name,source_reference,source_locator,term,marks,lecture_hours,non_lecture_hours,sort_order)
VALUES
('y1-pv-paper1','bams_ncism_1','2021-22','AyUG-PV',NULL,'paper','I','Paper I','NCISM AyUG-PV','Table 2: Contents of Course',NULL,NULL,NULL,NULL,10),
('y1-pv-1','bams_ncism_1','2021-22','AyUG-PV','y1-pv-paper1','unit','1','Ayurveda Nirupana','NCISM AyUG-PV','Table 2, topic 1',1,NULL,5,6,10),
('y1-pv-2','bams_ncism_1','2021-22','AyUG-PV','y1-pv-paper1','unit','2','Padartha and Darshana Nirupana','NCISM AyUG-PV','Table 2, topic 2',1,NULL,NULL,NULL,20),

('y1-rs-paper1','bams_ncism_1','2021-22','AyUG-RS',NULL,'paper','I','Paper I','NCISM AyUG-RS','Table 2: Contents of Course',NULL,NULL,NULL,NULL,10),
('y1-rs-1','bams_ncism_1','2021-22','AyUG-RS','y1-rs-paper1','unit','1','Shariropkramaniya Shaarira','NCISM AyUG-RS','Table 2, Paper I topic 1',1,6,4,2,10),
('y1-rs-2','bams_ncism_1','2021-22','AyUG-RS','y1-rs-paper1','unit','2','Paribhasha Shaarira','NCISM AyUG-RS','Table 2, Paper I topic 2',1,4,3,1,20),
('y1-rs-3','bams_ncism_1','2021-22','AyUG-RS','y1-rs-paper1','unit','3','Garbha Shaarira','NCISM AyUG-RS','Table 2, Paper I topic 3',1,15,17,5,30),

('y1-ks-paper1','bams_ncism_1','2021-22','AyUG-KS',NULL,'paper','I','Paper I','NCISM AyUG-KS','Table 2: Contents of Course',NULL,NULL,NULL,NULL,10),
('y1-ks-1','bams_ncism_1','2021-22','AyUG-KS','y1-ks-paper1','unit','1','Sharir','NCISM AyUG-KS','Table 2, topic 1',1,8,2,1,10),
('y1-ks-2','bams_ncism_1','2021-22','AyUG-KS','y1-ks-paper1','unit','2','Basic principles of Ayurveda','NCISM AyUG-KS','Table 2, topic 2',1,NULL,2,1,20),
('y1-ks-3','bams_ncism_1','2021-22','AyUG-KS','y1-ks-paper1','unit','3','Tridosha','NCISM AyUG-KS','Table 2, topic 3',1,NULL,3,0,30),

('y2-rb-paper1','bams_ncism_2','2021-22','AyUG-RB',NULL,'paper','I','Ayurvediya Aushadhi Nirmana Vigyana','NCISM AyUG-RB','Table 2: Paper 1',NULL,NULL,NULL,NULL,10),
('y2-rb-1','bams_ncism_2','2021-22','AyUG-RB','y2-rb-paper1','unit','1','Chronological development of Ayurvediya Aushadhi Nirmana','NCISM AyUG-RB','Table 2, topic 1',1,5,2,1,10),
('y2-rb-2','bams_ncism_2','2021-22','AyUG-RB','y2-rb-paper1','unit','2','Paribhasha (Terminology)','NCISM AyUG-RB','Table 2, topic 2',1,10,8,4,20),

('y2-at-paper1','bams_ncism_2','2021-22','AyUG-AT',NULL,'paper','I','Paper 1','NCISM AyUG-AT','Table 2: Paper 1',NULL,NULL,NULL,NULL,10),
('y2-at-1','bams_ncism_2','2021-22','AyUG-AT','y2-at-paper1','unit','1','Concepts of Agada Tantra (Clinical Toxicology)','NCISM AyUG-AT','Table 2, topic 1',1,13,8,1,10),
('y2-at-2','bams_ncism_2','2021-22','AyUG-AT','y2-at-paper1','unit','2','Visha Chikitsa (Management of Poisoning)','NCISM AyUG-AT','Table 2, topic 2',1,NULL,5,4,20),
('y2-at-3','bams_ncism_2','2021-22','AyUG-AT','y2-at-paper1','unit','3','Vishakta aahara pariksha and Viruddha ahara','NCISM AyUG-AT','Table 2, topic 3',1,NULL,3,2,30),

('y2-sa2-paper1','bams_ncism_2','2021-22','AyUG-SA2',NULL,'paper','I','Paper 1','NCISM AyUG-SA2','Table 2: Paper 1',NULL,NULL,NULL,NULL,10),
('y2-sa2-1','bams_ncism_2','2021-22','AyUG-SA2','y2-sa2-paper1','chapter','Cha.Su.13','Sneha Adhyaya','NCISM AyUG-SA2','Table 2, topic 1',1,37,3,1,10),
('y2-sa2-2','bams_ncism_2','2021-22','AyUG-SA2','y2-sa2-paper1','chapter','Cha.Su.14','Sveda Adhyaya','NCISM AyUG-SA2','Table 2, topic 2',1,NULL,2,1,20),
('y2-sa2-3','bams_ncism_2','2021-22','AyUG-SA2','y2-sa2-paper1','chapter','Cha.Su.15','Upakalpaneeya Adhyaya','NCISM AyUG-SA2','Table 2, topic 3',1,NULL,2,3,30),

('y2-dg-paper1','bams_ncism_2','2021-22','AyUG-DG',NULL,'paper','I','Fundamental Dravyaguna','NCISM AyUG-DG','Table 2: Paper 1',NULL,NULL,NULL,NULL,10),
('y2-dg-1','bams_ncism_2','2021-22','AyUG-DG','y2-dg-paper1','unit','1','Dravyaguna Vigyana','NCISM AyUG-DG','Table 2, topic 1',1,1,1,1,10),
('y2-dg-2','bams_ncism_2','2021-22','AyUG-DG','y2-dg-paper1','unit','2','Dravya','NCISM AyUG-DG','Table 2, topic 2',1,6,5,4,20),
('y2-dg-3','bams_ncism_2','2021-22','AyUG-DG','y2-dg-paper1','unit','3','Guna','NCISM AyUG-DG','Table 2, topic 3',1,11,4,2,30),
('y2-dg-4','bams_ncism_2','2021-22','AyUG-DG','y2-dg-paper1','unit','4','Rasa','NCISM AyUG-DG','Table 2, topic 4',1,11,7,4,40),

('y2-sw-paper1','bams_ncism_2','2021-22','AyUG-SW',NULL,'paper','I','Principles of Swasthavritta, Yoga and Naturopathy','NCISM AyUG-SW','Table 2: Paper 1',NULL,NULL,NULL,NULL,10),
('y2-sw-1','bams_ncism_2','2021-22','AyUG-SW','y2-sw-paper1','unit','1','Swastha and Swasthya','NCISM AyUG-SW','Table 2, topic 1',1,6,3,0,10),
('y2-sw-2','bams_ncism_2','2021-22','AyUG-SW','y2-sw-paper1','unit','2','Healthy Life style - Dinacharya (Daily regimen)','NCISM AyUG-SW','Table 2, topic 2',1,38,8,5,20);
