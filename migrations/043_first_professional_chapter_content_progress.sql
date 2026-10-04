INSERT OR IGNORE INTO curriculum_nodes
(node_id,curriculum_id,curriculum_version,subject_id,parent_node_id,node_type,code,name,source_reference,source_locator,term,marks,lecture_hours,non_lecture_hours,sort_order)
VALUES ('y1-sa1-3','bams_ncism_1','2021-22','AyUG-SA1','y1-sa1-paper1','chapter','AH.Su.2','Dinacharya Adhyaya','NCISM AyUG-SA1','Table 2, Ashtanga Hridaya Sutrasthana 2',1,50,8,3,30);

-- NCISM first-professional content progress markers.
UPDATE curriculum_nodes
SET status = 'content_complete_student_layer'
WHERE curriculum_id = 'bams_ncism_1'
  AND curriculum_version = '2021-22'
  AND subject_id = 'AyUG-SA1'
  AND node_id = 'y1-sa1-2';

UPDATE curriculum_nodes SET status = 'content_complete_student_layer'
WHERE curriculum_id = 'bams_ncism_1' AND curriculum_version = '2021-22'
  AND subject_id = 'AyUG-SA1' AND node_id = 'y1-sa1-3';
