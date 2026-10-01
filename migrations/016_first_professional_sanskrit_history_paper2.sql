-- Structural partitions for AyUG-SN & AI Paper II; detailed topic content remains source-ingestion work.
INSERT OR IGNORE INTO curriculum_nodes
(node_id,curriculum_id,curriculum_version,subject_id,parent_node_id,node_type,code,name,source_reference,source_locator,term,sort_order)
VALUES
('y1-snai2-a','bams_ncism_1','2021-22','AyUG-SN-AI','y1-sn-ai-paper2','unit','A','Sanskrit','NCISM AyUG-SN & AI','Paper II Part A',1,10),
('y1-snai2-b','bams_ncism_1','2021-22','AyUG-SN-AI','y1-sn-ai-paper2','unit','B','Ayurved Itihas','NCISM AyUG-SN & AI','Paper II Part B',2,20);
