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


-- NCISM first-professional Chapter 3 content marker.
INSERT OR IGNORE INTO curriculum_nodes
(node_id,curriculum_id,curriculum_version,subject_id,parent_node_id,node_type,code,name,source_reference,source_locator,term,marks,lecture_hours,non_lecture_hours,sort_order)
VALUES ('y1-sa1-4','bams_ncism_1','2021-22','AyUG-SA1','y1-sa1-paper1','chapter','AH.Su.3','Ritucharya Adhyaya','NCISM AyUG-SA1','Table 2, Ashtanga Hridaya Sutrasthana 3',1,50,5,4,40);

UPDATE curriculum_nodes SET status = 'content_complete_student_layer'
WHERE curriculum_id = 'bams_ncism_1' AND curriculum_version = '2021-22'
  AND subject_id = 'AyUG-SA1' AND node_id = 'y1-sa1-4';

-- NCISM first-professional Chapter 4 content marker.
INSERT OR IGNORE INTO curriculum_nodes
(node_id,curriculum_id,curriculum_version,subject_id,parent_node_id,node_type,code,name,source_reference,source_locator,term,marks,lecture_hours,non_lecture_hours,sort_order)
VALUES ('y1-sa1-5','bams_ncism_1','2021-22','AyUG-SA1','y1-sa1-paper1','chapter','AH.Su.4','Roganutpadaniya Adhyaya','NCISM AyUG-SA1','Table 2, Ashtanga Hridaya Sutrasthana 4',1,50,5,4,50);

UPDATE curriculum_nodes SET status = 'content_complete_student_layer'
WHERE curriculum_id = 'bams_ncism_1' AND curriculum_version = '2021-22'
  AND subject_id = 'AyUG-SA1' AND node_id = 'y1-sa1-5';

-- NCISM first-professional Chapter 5 content marker.
INSERT OR IGNORE INTO curriculum_nodes
(node_id,curriculum_id,curriculum_version,subject_id,parent_node_id,node_type,code,name,source_reference,source_locator,term,marks,lecture_hours,non_lecture_hours,sort_order)
VALUES ('y1-sa1-6','bams_ncism_1','2021-22','AyUG-SA1','y1-sa1-paper1','chapter','AH.Su.5','Dravadravya Vijnaniya Adhyaya','NCISM AyUG-SA1','Table 2, Ashtanga Hridaya Sutrasthana 5',1,50,5,4,60);

UPDATE curriculum_nodes SET status = 'content_complete_student_layer'
WHERE curriculum_id = 'bams_ncism_1' AND curriculum_version = '2021-22'
  AND subject_id = 'AyUG-SA1' AND node_id = 'y1-sa1-6';

-- NCISM first-professional Chapter 6 content marker.
INSERT OR IGNORE INTO curriculum_nodes
(node_id,curriculum_id,curriculum_version,subject_id,parent_node_id,node_type,code,name,source_reference,source_locator,term,marks,lecture_hours,non_lecture_hours,sort_order)
VALUES ('y1-sa1-7','bams_ncism_1','2021-22','AyUG-SA1','y1-sa1-paper1','chapter','AH.Su.6','Annasvarupa Vijnaniya Adhyaya','NCISM AyUG-SA1','Table 2, Ashtanga Hridaya Sutrasthana 6',1,50,5,4,70);

UPDATE curriculum_nodes SET status = 'content_complete_student_layer'
WHERE curriculum_id = 'bams_ncism_1' AND curriculum_version = '2021-22'
  AND subject_id = 'AyUG-SA1' AND node_id = 'y1-sa1-7';

-- NCISM first-professional Chapter 7 content marker.
INSERT OR IGNORE INTO curriculum_nodes
(node_id,curriculum_id,curriculum_version,subject_id,parent_node_id,node_type,code,name,source_reference,source_locator,term,marks,lecture_hours,non_lecture_hours,sort_order)
VALUES ('y1-sa1-8','bams_ncism_1','2021-22','AyUG-SA1','y1-sa1-paper1','chapter','AH.Su.7','Annaraksha Adhyaya','NCISM AyUG-SA1','Table 2, Ashtanga Hridaya Sutrasthana 7',1,50,5,4,80);

UPDATE curriculum_nodes SET status = 'content_complete_student_layer'
WHERE curriculum_id = 'bams_ncism_1' AND curriculum_version = '2021-22'
  AND subject_id = 'AyUG-SA1' AND node_id = 'y1-sa1-8';

-- NCISM first-professional Chapter 8 content marker.
INSERT OR IGNORE INTO curriculum_nodes
(node_id,curriculum_id,curriculum_version,subject_id,parent_node_id,node_type,code,name,source_reference,source_locator,term,marks,lecture_hours,non_lecture_hours,sort_order)
VALUES ('y1-sa1-9','bams_ncism_1','2021-22','AyUG-SA1','y1-sa1-paper1','chapter','AH.Su.8','Matrashitiya Adhyaya','NCISM AyUG-SA1','Table 2, Ashtanga Hridaya Sutrasthana 8',1,50,5,4,90);

UPDATE curriculum_nodes SET status = 'content_complete_student_layer'
WHERE curriculum_id = 'bams_ncism_1' AND curriculum_version = '2021-22'
  AND subject_id = 'AyUG-SA1' AND node_id = 'y1-sa1-9';

-- NCISM first-professional Chapter 9 content marker.
INSERT OR IGNORE INTO curriculum_nodes
(node_id,curriculum_id,curriculum_version,subject_id,parent_node_id,node_type,code,name,source_reference,source_locator,term,marks,lecture_hours,non_lecture_hours,sort_order)
VALUES ('y1-sa1-10','bams_ncism_1','2021-22','AyUG-SA1','y1-sa1-paper1','chapter','AH.Su.9','Dravyadi Vijnaniya Adhyaya','NCISM AyUG-SA1','Table 2, Ashtanga Hridaya Sutrasthana 9',1,50,5,4,100);

UPDATE curriculum_nodes SET status = 'content_complete_student_layer'
WHERE curriculum_id = 'bams_ncism_1' AND curriculum_version = '2021-22'
  AND subject_id = 'AyUG-SA1' AND node_id = 'y1-sa1-10';
