-- NCISM-verified structural chapter anchors for AyUG-SA3.
-- Detailed content remains linked to source references and can be expanded without changing hierarchy.
INSERT OR IGNORE INTO curriculum_nodes
(node_id,curriculum_id,curriculum_version,subject_id,parent_node_id,node_type,code,name,source_reference,source_locator,sort_order)
VALUES
('y3-sa3-samhita','bams_ncism_3','2021-22','AyUG-SA3','y3-sa3-paper1','unit','SA3','Samhita Adhyayan-3: classical text study and applied interpretation','NCISM AyUG-SA3','Official curriculum structure',10),
('y3-sa3-samhita-charaka','bams_ncism_3','2021-22','AyUG-SA3','y3-sa3-samhita','chapter','Charaka','Charaka Samhita selections','NCISM AyUG-SA3','Official curriculum structure',20),
('y3-sa3-samhita-sushruta','bams_ncism_3','2021-22','AyUG-SA3','y3-sa3-samhita','chapter','Sushruta','Sushruta Samhita selections','NCISM AyUG-SA3','Official curriculum structure',30),
('y3-sa3-samhita-ashtanga','bams_ncism_3','2021-22','AyUG-SA3','y3-sa3-samhita','chapter','AH','Ashtanga Hridaya selections','NCISM AyUG-SA3','Official curriculum structure',40);