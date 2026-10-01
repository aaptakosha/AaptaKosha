-- NCISM-verified third-professional paper metadata.
-- Detailed topic ingestion remains source-verified per subject before insertion.
INSERT OR IGNORE INTO curriculum_nodes
(node_id,curriculum_id,curriculum_version,subject_id,parent_node_id,node_type,code,name,source_reference,source_locator,sort_order)
VALUES
('y3-pk-paper1','bams_ncism_3','2021-22','AyUG-PK',NULL,'paper','I','Paper I','NCISM AyUG-PK','Summary / Examination',10),
('y3-st-paper1','bams_ncism_3','2021-22','AyUG-ST',NULL,'paper','I','Paper I','NCISM AyUG-ST','Summary / Examination',10),
('y3-st-paper2','bams_ncism_3','2021-22','AyUG-ST',NULL,'paper','II','Paper II','NCISM AyUG-ST','Summary / Examination',20),
('y3-sl-paper1','bams_ncism_3','2021-22','AyUG-SL',NULL,'paper','I','Paper I','NCISM AyUG-SL','Question Paper Pattern',10),
('y3-sl-paper2','bams_ncism_3','2021-22','AyUG-SL',NULL,'paper','II','Paper II','NCISM AyUG-SL','Question Paper Pattern',20);