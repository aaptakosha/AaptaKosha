-- Verified NCISM paper-level metadata for AyUG-KB.
-- Topic-level expansion is kept source-verified before insertion.
INSERT OR IGNORE INTO curriculum_nodes
(node_id,curriculum_id,curriculum_version,subject_id,parent_node_id,node_type,code,name,source_reference,source_locator,sort_order)
VALUES
('y3-kb-paper1','bams_ncism_3','2021-22','AyUG-KB',NULL,'paper','I','Paper I','NCISM AyUG-KB','Question Paper Pattern',10);