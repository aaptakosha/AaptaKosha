-- Align AyUG-SW with the corrected NCISM Table 2 course-content structure.
-- The prior A-F rows represented assessment/viva grouping rather than the syllabus topic hierarchy.
DELETE FROM curriculum_nodes
WHERE curriculum_id='bams_ncism_2'
  AND subject_id='AyUG-SW'
  AND parent_node_id IN ('y2-sw-paper1','y2-sw-paper2');

INSERT OR IGNORE INTO curriculum_nodes
(node_id,curriculum_id,curriculum_version,subject_id,parent_node_id,node_type,code,name,source_reference,source_locator,sort_order)
VALUES
('y2-sw1-topic-01','bams_ncism_2','2021-22','AyUG-SW','y2-sw-paper1','topic','1','Swastha and Swasthya','NCISM AyUG-SW','Table 2 Paper 1',10),
('y2-sw1-topic-02','bams_ncism_2','2021-22','AyUG-SW','y2-sw-paper1','topic','2','Healthy Life style - Dinacharya (Daily regimen)','NCISM AyUG-SW','Table 2 Paper 1',20),
('y2-sw1-topic-03','bams_ncism_2','2021-22','AyUG-SW','y2-sw-paper1','topic','3','Ratricharya','NCISM AyUG-SW','Table 2 Paper 1',30),
('y2-sw1-topic-04','bams_ncism_2','2021-22','AyUG-SW','y2-sw-paper1','topic','4','Ritucharya','NCISM AyUG-SW','Table 2 Paper 1',40),
('y2-sw1-topic-05','bams_ncism_2','2021-22','AyUG-SW','y2-sw-paper1','topic','5','Roganutpadaniya','NCISM AyUG-SW','Table 2 Paper 1',50),
('y2-sw1-topic-06','bams_ncism_2','2021-22','AyUG-SW','y2-sw-paper1','topic','6','Sadvritta','NCISM AyUG-SW','Table 2 Paper 1',60),
('y2-sw1-topic-07','bams_ncism_2','2021-22','AyUG-SW','y2-sw-paper1','topic','7','Ahara','NCISM AyUG-SW','Table 2 Paper 1',70),
('y2-sw1-topic-08','bams_ncism_2','2021-22','AyUG-SW','y2-sw-paper1','topic','8','Rasayana for Swastha','NCISM AyUG-SW','Table 2 Paper 1',80),
('y2-sw1-topic-09','bams_ncism_2','2021-22','AyUG-SW','y2-sw-paper1','topic','9','Yoga','NCISM AyUG-SW','Table 2 Paper 1',90),
('y2-sw1-topic-10','bams_ncism_2','2021-22','AyUG-SW','y2-sw-paper1','topic','10','Naturopathy','NCISM AyUG-SW','Table 2 Paper 1',100),
('y2-sw2-topic-11','bams_ncism_2','2021-22','AyUG-SW','y2-sw-paper2','topic','11','Janapadodhwamsa / Maraka Vyadhi','NCISM AyUG-SW','Table 2 Paper 2',10),
('y2-sw2-topic-12','bams_ncism_2','2021-22','AyUG-SW','y2-sw-paper2','topic','12','Environmental health','NCISM AyUG-SW','Table 2 Paper 2',20),
('y2-sw2-topic-13','bams_ncism_2','2021-22','AyUG-SW','y2-sw-paper2','topic','13','Disaster management','NCISM AyUG-SW','Table 2 Paper 2',30),
('y2-sw2-topic-14','bams_ncism_2','2021-22','AyUG-SW','y2-sw-paper2','topic','14','Occupational Health','NCISM AyUG-SW','Table 2 Paper 2',40),
('y2-sw2-topic-15','bams_ncism_2','2021-22','AyUG-SW','y2-sw-paper2','topic','15','School health services','NCISM AyUG-SW','Table 2 Paper 2',50),
('y2-sw2-topic-16','bams_ncism_2','2021-22','AyUG-SW','y2-sw-paper2','topic','16','Disinfection','NCISM AyUG-SW','Table 2 Paper 2',60),
('y2-sw2-topic-17','bams_ncism_2','2021-22','AyUG-SW','y2-sw-paper2','topic','17','Primary health care','NCISM AyUG-SW','Table 2 Paper 2',70),
('y2-sw2-topic-18','bams_ncism_2','2021-22','AyUG-SW','y2-sw-paper2','topic','18','Mother and Child health care','NCISM AyUG-SW','Table 2 Paper 2',80),
('y2-sw2-topic-19','bams_ncism_2','2021-22','AyUG-SW','y2-sw-paper2','topic','19','Family welfare programme','NCISM AyUG-SW','Table 2 Paper 2',90),
('y2-sw2-topic-20','bams_ncism_2','2021-22','AyUG-SW','y2-sw-paper2','topic','20','Preventive Geriatrics','NCISM AyUG-SW','Table 2 Paper 2',100),
('y2-sw2-topic-21','bams_ncism_2','2021-22','AyUG-SW','y2-sw-paper2','topic','21','World Health Organization and International health agencies','NCISM AyUG-SW','Table 2 Paper 2',110),
('y2-sw2-topic-22','bams_ncism_2','2021-22','AyUG-SW','y2-sw-paper2','topic','22','Vital Statistics','NCISM AyUG-SW','Table 2 Paper 2',120),
('y2-sw2-topic-23','bams_ncism_2','2021-22','AyUG-SW','y2-sw-paper2','topic','23','Health Administration','NCISM AyUG-SW','Table 2 Paper 2',130),
('y2-sw2-topic-24','bams_ncism_2','2021-22','AyUG-SW','y2-sw-paper2','topic','24','National Health Programmes','NCISM AyUG-SW','Table 2 Paper 2',140),
('y2-sw2-topic-25','bams_ncism_2','2021-22','AyUG-SW','y2-sw-paper2','topic','25','National Health Policy','NCISM AyUG-SW','Table 2 Paper 2',150);
