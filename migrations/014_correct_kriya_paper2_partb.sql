-- Correct the earlier Kriya Paper II seed: topics 1-16 are Ayurveda/Kriya theory;
-- contemporary physiology is the separate Part-B sequence 1-8.
DELETE FROM curriculum_nodes
WHERE curriculum_id='bams_ncism_1' AND subject_id='AyUG-KS'
  AND parent_node_id='y1-ks2-paper2'
  AND node_id IN ('y1-ks2-17','y1-ks2-18','y1-ks2-19','y1-ks2-20','y1-ks2-21','y1-ks2-22','y1-ks2-23','y1-ks2-24');

INSERT OR IGNORE INTO curriculum_nodes
(node_id,curriculum_id,curriculum_version,subject_id,parent_node_id,node_type,code,name,source_reference,source_locator,term,sort_order)
VALUES
('y1-ks2-b1','bams_ncism_1','2021-22','AyUG-KS','y1-ks2-paper2','unit','B1','Haemopoetic system','NCISM AyUG-KS','Paper II Part-B topic 1',1,101),
('y1-ks2-b2','bams_ncism_1','2021-22','AyUG-KS','y1-ks2-paper2','unit','B2','Immunity','NCISM AyUG-KS','Paper II Part-B topic 2',1,102),
('y1-ks2-b3','bams_ncism_1','2021-22','AyUG-KS','y1-ks2-paper2','unit','B3','Physiology of cardio-vascular system','NCISM AyUG-KS','Paper II Part-B topic 3',1,103),
('y1-ks2-b4','bams_ncism_1','2021-22','AyUG-KS','y1-ks2-paper2','unit','B4','Muscle physiology','NCISM AyUG-KS','Paper II Part-B topic 4',2,104),
('y1-ks2-b5','bams_ncism_1','2021-22','AyUG-KS','y1-ks2-paper2','unit','B5','Adipose tissue','NCISM AyUG-KS','Paper II Part-B topic 5',2,105),
('y1-ks2-b6','bams_ncism_1','2021-22','AyUG-KS','y1-ks2-paper2','unit','B6','Physiology of male and female reproductive systems','NCISM AyUG-KS','Paper II Part-B topic 6',2,106),
('y1-ks2-b7','bams_ncism_1','2021-22','AyUG-KS','y1-ks2-paper2','unit','B7','Physiology of Excretion','NCISM AyUG-KS','Paper II Part-B topic 7',3,107),
('y1-ks2-b8','bams_ncism_1','2021-22','AyUG-KS','y1-ks2-paper2','unit','B8','Special Senses, Sleep and Dreams','NCISM AyUG-KS','Paper II Part-B topic 8',3,108);
