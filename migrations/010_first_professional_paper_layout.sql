-- First-professional paper layout anchors verified from NCISM examination sections.
-- Detailed topic content remains source-ingestion work and is intentionally deferred.
INSERT OR IGNORE INTO curriculum_nodes
(node_id,curriculum_id,curriculum_version,subject_id,parent_node_id,node_type,code,name,source_reference,source_locator,term,marks,lecture_hours,non_lecture_hours,sort_order)
VALUES
('y1-pv-paper2','bams_ncism_1','2021-22','AyUG-PV',NULL,'paper','II','Paper II','NCISM AyUG-PV','E-Paper Layout, Paper II',NULL,NULL,NULL,NULL,20),
('y1-rs-paper2','bams_ncism_1','2021-22','AyUG-RS',NULL,'paper','II','Paper II','NCISM AyUG-RS','E-Paper Layout, Paper II',NULL,NULL,NULL,NULL,20),
('y1-ks-paper2','bams_ncism_1','2021-22','AyUG-KS',NULL,'paper','II','Paper II','NCISM AyUG-KS','E-Paper Layout, Paper II',NULL,NULL,NULL,NULL,20),
('y1-sn-ai-paper1','bams_ncism_1','2021-22','AyUG-SN-AI',NULL,'paper','I','Paper I','NCISM AyUG-SN & AI','Summary / Examination (Papers & Mark Distribution)',NULL,NULL,NULL,NULL,10),
('y1-sn-ai-paper2','bams_ncism_1','2021-22','AyUG-SN-AI',NULL,'paper','II','Paper II','NCISM AyUG-SN & AI','Summary / Examination (Papers & Mark Distribution)',NULL,NULL,NULL,NULL,20);
