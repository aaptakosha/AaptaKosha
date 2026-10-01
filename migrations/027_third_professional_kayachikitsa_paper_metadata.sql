-- Verified NCISM paper-level metadata for AyUG-KC.
-- Three theory papers; detailed topic ingestion is performed only from verified source tables.
INSERT OR IGNORE INTO curriculum_nodes
(node_id,curriculum_id,curriculum_version,subject_id,parent_node_id,node_type,code,name,source_reference,source_locator,sort_order)
VALUES
('y3-kc-paper1','bams_ncism_3','2021-22','AyUG-KC',NULL,'paper','I','Paper I','NCISM AyUG-KC','Examination / Theory',10),
('y3-kc-paper2','bams_ncism_3','2021-22','AyUG-KC',NULL,'paper','II','Paper II','NCISM AyUG-KC','Examination / Theory',20),
('y3-kc-paper3','bams_ncism_3','2021-22','AyUG-KC',NULL,'paper','III','Paper III','NCISM AyUG-KC','Examination / Theory',30);