-- NCISM-verified complete AyUG-KB Paper I hierarchy and teaching metadata.
-- Source: official NCISM AyUG-KB Table 2, Paper I.
UPDATE curriculum_nodes SET term='1', marks=1, lecture_hours=2, non_lecture_hours=0 WHERE node_id='y3-kb-1';
UPDATE curriculum_nodes SET term='1', marks=7, lecture_hours=5, non_lecture_hours=16 WHERE node_id='y3-kb-2';
UPDATE curriculum_nodes SET term='1', marks=11, lecture_hours=13, non_lecture_hours=15 WHERE node_id='y3-kb-3';
UPDATE curriculum_nodes SET term='1', marks=11, lecture_hours=5, non_lecture_hours=9 WHERE node_id='y3-kb-4';
UPDATE curriculum_nodes SET term='1', marks=5, lecture_hours=5, non_lecture_hours=13 WHERE node_id='y3-kb-5';
UPDATE curriculum_nodes SET term='2', marks=7, lecture_hours=6, non_lecture_hours=7 WHERE node_id='y3-kb-6';
UPDATE curriculum_nodes SET term='2', marks=5, lecture_hours=0, non_lecture_hours=16 WHERE node_id='y3-kb-7';
UPDATE curriculum_nodes SET term='2', marks=5, lecture_hours=5, non_lecture_hours=7 WHERE node_id='y3-kb-8';
UPDATE curriculum_nodes SET term='2', marks=8, lecture_hours=7, non_lecture_hours=7 WHERE node_id='y3-kb-9';

INSERT OR IGNORE INTO curriculum_nodes
(node_id,curriculum_id,curriculum_version,subject_id,parent_node_id,node_type,code,name,source_reference,source_locator,term,marks,lecture_hours,non_lecture_hours,sort_order)
VALUES
('y3-kb-10','bams_ncism_3','2021-22','AyUG-KB','y3-kb-paper1','topic','10','Swasana Rogas [Disorders of Respiratory system]','NCISM AyUG-KB','Table 2: Contents of Course, Paper 1','2',10,5,10,100),
('y3-kb-11','bams_ncism_3','2021-22','AyUG-KB','y3-kb-paper1','topic','11','Mahasrota Roga [Gastro Intestinal Disorders]','NCISM AyUG-KB','Table 2: Contents of Course, Paper 1','2',6,3,9,110),
('y3-kb-12','bams_ncism_3','2021-22','AyUG-KB','y3-kb-paper1','topic','12','Rasa Rakta Rogas [Disorders of blood and cardiovascular system]','NCISM AyUG-KB','Table 2: Contents of Course, Paper 1','2',10,3,9,120),
('y3-kb-13','bams_ncism_3','2021-22','AyUG-KB','y3-kb-paper1','topic','13','Antahsravee Granthi Rogas (Disorders of Endocrine System)','NCISM AyUG-KB','Table 2: Contents of Course, Paper 1','2',3,2,4,130),
('y3-kb-14','bams_ncism_3','2021-22','AyUG-KB','y3-kb-paper1','topic','14','Mutravaha Sroto Rogas (Disorders of Genito urinary system)','NCISM AyUG-KB','Table 2: Contents of Course, Paper 1','3',5,3,4,140),
('y3-kb-15','bams_ncism_3','2021-22','AyUG-KB','y3-kb-paper1','topic','15','Sandhi Rogas (Rheumatological Disorders)','NCISM AyUG-KB','Table 2: Contents of Course, Paper 1','3',3,2,4,150),
('y3-kb-16','bams_ncism_3','2021-22','AyUG-KB','y3-kb-paper1','topic','16','Twak Rogas (Dermatological Disorders)','NCISM AyUG-KB','Table 2: Contents of Course, Paper 1','3',13,3,5,160),
('y3-kb-17','bams_ncism_3','2021-22','AyUG-KB','y3-kb-paper1','topic','17','Sira Snayu Rogas (Nervous system disorders)','NCISM AyUG-KB','Table 2: Contents of Course, Paper 1','3',7,3,12,170),
('y3-kb-18','bams_ncism_3','2021-22','AyUG-KB','y3-kb-paper1','topic','18','Unmada Rogas (Behavioral and Neurobehavioral disorders)','NCISM AyUG-KB','Table 2: Contents of Course, Paper 1','3',3,4,9,180),
('y3-kb-19','bams_ncism_3','2021-22','AyUG-KB','y3-kb-paper1','topic','19','Atyayika Rogas (Emergency Paediatrics)','NCISM AyUG-KB','Table 2: Contents of Course, Paper 1','3',12,3,5,190),
('y3-kb-20','bams_ncism_3','2021-22','AyUG-KB','y3-kb-paper1','topic','20','Bala Panchakarma','NCISM AyUG-KB','Table 2: Contents of Course, Paper 1','3',5,0,8,200),
('y3-kb-21','bams_ncism_3','2021-22','AyUG-KB','y3-kb-paper1','topic','21','Kishora Swasthya (Adolescent Health)','NCISM AyUG-KB','Table 2: Contents of Course, Paper 1','3',2,0,1,210),
('y3-kb-22','bams_ncism_3','2021-22','AyUG-KB','y3-kb-paper1','topic','22','Anya Rogas (Miscellaneous Diseases)','NCISM AyUG-KB','Table 2: Contents of Course, Paper 1','3',1,1,1,220);
