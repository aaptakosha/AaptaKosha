-- Third-professional paper layout anchors verified against current NCISM course summaries.
-- Detailed units/chapters/topics remain intentionally deferred until source ingestion.
INSERT OR IGNORE INTO curriculum_nodes
(node_id,curriculum_id,curriculum_version,subject_id,parent_node_id,node_type,code,name,source_reference,source_locator,term,marks,lecture_hours,non_lecture_hours,sort_order)
VALUES
('y3-kc-paper1','bams_ncism_3','2021-22','AyUG-KC',NULL,'paper','I','Paper I','NCISM AyUG-KC','Course summary: Paper I',NULL,NULL,NULL,NULL,10),
('y3-kc-paper2','bams_ncism_3','2021-22','AyUG-KC',NULL,'paper','II','Paper II','NCISM AyUG-KC','Course summary: Paper II',NULL,NULL,NULL,NULL,20),
('y3-kc-paper3','bams_ncism_3','2021-22','AyUG-KC',NULL,'paper','III','Paper III','NCISM AyUG-KC','Course summary: Paper III',NULL,NULL,NULL,NULL,30),

('y3-pk-paper1','bams_ncism_3','2021-22','AyUG-PK',NULL,'paper','I','Paper I','NCISM AyUG-PK','Course summary: Paper I',NULL,NULL,NULL,NULL,10),

('y3-st-paper1','bams_ncism_3','2021-22','AyUG-ST',NULL,'paper','I','Paper I','NCISM AyUG-ST','Course summary: Paper I',NULL,NULL,NULL,NULL,10),
('y3-st-paper2','bams_ncism_3','2021-22','AyUG-ST',NULL,'paper','II','Paper II','NCISM AyUG-ST','Course summary: Paper II',NULL,NULL,NULL,NULL,20),

('y3-sl-paper1','bams_ncism_3','2021-22','AyUG-SL',NULL,'paper','I','Paper I','NCISM AyUG-SL','Course summary: Paper I',NULL,NULL,NULL,NULL,10),
('y3-sl-paper2','bams_ncism_3','2021-22','AyUG-SL',NULL,'paper','II','Paper II','NCISM AyUG-SL','Course summary: Paper II',NULL,NULL,NULL,NULL,20),

('y3-ps-paper1','bams_ncism_3','2021-22','AyUG-PS',NULL,'paper','I','Paper I','NCISM AyUG-PS','Course summary: Paper I',NULL,NULL,NULL,NULL,10),
('y3-ps-paper2','bams_ncism_3','2021-22','AyUG-PS',NULL,'paper','II','Paper II','NCISM AyUG-PS','Course summary: Paper II',NULL,NULL,NULL,NULL,20),

('y3-kb-paper1','bams_ncism_3','2021-22','AyUG-KB',NULL,'paper','I','Paper I','NCISM AyUG-KB','Course summary: Paper I',NULL,NULL,NULL,NULL,10),

('y3-sa3-paper1','bams_ncism_3','2021-22','AyUG-SA3',NULL,'paper','I','Paper I','NCISM AyUG-SA3','Course summary: Paper I',NULL,NULL,NULL,NULL,10),

('y3-rm-paper1','bams_ncism_3','2021-22','AyUG-RM',NULL,'paper','I','Paper I','NCISM AyUG-RM','Course summary: Paper I',NULL,NULL,NULL,NULL,10),

('y3-em-paper1','bams_ncism_3','2021-22','AyUG-EM',NULL,'paper','I','Paper I','NCISM AyUG-EM','Course summary: Paper I',NULL,NULL,NULL,NULL,10);
