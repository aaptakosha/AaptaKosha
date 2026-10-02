-- Second-professional paper layout anchors verified from NCISM assessment sections.
-- Topic-level content remains source-ingestion work and is intentionally deferred.
INSERT OR IGNORE INTO curriculum_nodes
(node_id,curriculum_id,curriculum_version,subject_id,parent_node_id,node_type,code,name,source_reference,source_locator,term,marks,lecture_hours,non_lecture_hours,sort_order)
VALUES
('y2-rb-paper1','bams_ncism_2','2021-22','AyUG-RB',NULL,'paper','I','Paper I','NCISM AyUG-RB','Question paper pattern / distribution of theory examination',NULL,NULL,NULL,NULL,10),
('y2-rb-paper2','bams_ncism_2','2021-22','AyUG-RB',NULL,'paper','II','Paper II','NCISM AyUG-RB','Question paper pattern / distribution of theory examination',NULL,NULL,NULL,NULL,20),
('y2-at-paper1','bams_ncism_2','2021-22','AyUG-AT',NULL,'paper','I','Paper I','NCISM AyUG-AT','Question paper pattern / distribution of theory examination',NULL,NULL,NULL,NULL,10),
('y2-sa2-paper1','bams_ncism_2','2021-22','AyUG-SA2',NULL,'paper','I','Paper I','NCISM AyUG-SA2','Question paper pattern / distribution of theory examination',NULL,NULL,NULL,NULL,10),
('y2-dg-paper1','bams_ncism_2','2021-22','AyUG-DG',NULL,'paper','I','Paper I','NCISM AyUG-DG','Question paper pattern / distribution of theory examination',NULL,NULL,NULL,NULL,10),
('y2-dg-paper2','bams_ncism_2','2021-22','AyUG-DG',NULL,'paper','II','Paper II','NCISM AyUG-DG','Question paper pattern / distribution of theory examination',NULL,NULL,NULL,NULL,20),
('y2-rn-paper1','bams_ncism_2','2021-22','AyUG-RN',NULL,'paper','I','Paper I','NCISM AyUG-RN','Question paper pattern / distribution of theory examination',NULL,NULL,NULL,NULL,10),
('y2-rn-paper2','bams_ncism_2','2021-22','AyUG-RN',NULL,'paper','II','Paper II','NCISM AyUG-RN','Question paper pattern / distribution of theory examination',NULL,NULL,NULL,NULL,20),
('y2-sw-paper1','bams_ncism_2','2021-22','AyUG-SW',NULL,'paper','I','Paper I','NCISM AyUG-SW','Question paper pattern / distribution of theory examination',NULL,NULL,NULL,NULL,10),
('y2-sw-paper2','bams_ncism_2','2021-22','AyUG-SW',NULL,'paper','II','Paper II','NCISM AyUG-SW','Question paper pattern / distribution of theory examination',NULL,NULL,NULL,NULL,20);
