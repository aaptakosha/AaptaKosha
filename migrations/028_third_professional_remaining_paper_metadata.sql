-- Verified NCISM paper-level metadata for remaining third-professional subjects.
-- Detailed topic ingestion remains source-verified before insertion.
INSERT OR IGNORE INTO curriculum_nodes
(node_id,curriculum_id,curriculum_version,subject_id,parent_node_id,node_type,code,name,source_reference,source_locator,sort_order)
VALUES
('y3-em-paper1','bams_ncism_3','2021-22','AyUG-EM',NULL,'paper','I','Paper I','NCISM AyUG-EM','Examination / Theory',10),
('y3-rm-paper1','bams_ncism_3','2021-22','AyUG-RM',NULL,'paper','I','Paper I','NCISM AyUG-RM','Examination / Theory',10),
('y3-sa3-paper1','bams_ncism_3','2021-22','AyUG-SA3',NULL,'paper','I','Paper I','NCISM AyUG-SA3','Examination / Theory',10);