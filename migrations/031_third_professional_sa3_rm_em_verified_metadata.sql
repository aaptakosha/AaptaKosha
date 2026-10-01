-- NCISM-verified metadata from official III Professional curriculum PDFs.
UPDATE curriculum_nodes SET lecture_hours=25, non_lecture_hours=50 WHERE node_id='y3-rm-paper1';

INSERT OR IGNORE INTO curriculum_nodes
(node_id,curriculum_id,curriculum_version,subject_id,parent_node_id,node_type,code,name,source_reference,source_locator,marks,sort_order)
VALUES
('y3-em-1','bams_ncism_3','2021-22','AyUG-EM','y3-em-paper1','topic','1','Atyayika Chikitsa: emergency assessment and management','NCISM AyUG-EM','Official curriculum Paper I',NULL,10),
('y3-em-2','bams_ncism_3','2021-22','AyUG-EM','y3-em-paper1','topic','2','Murcha (Syncope)','NCISM AyUG-EM','Official curriculum Paper I',2,20),
('y3-em-3','bams_ncism_3','2021-22','AyUG-EM','y3-em-paper1','topic','3','Akshepaka, Apasmara Vega (Convulsions, Status epilepticus)','NCISM AyUG-EM','Official curriculum Paper I',2,30),
('y3-em-4','bams_ncism_3','2021-22','AyUG-EM','y3-em-paper1','topic','4','Prameha Upadrava: DKA, HHS, hypoglycaemia and hyperglycaemia','NCISM AyUG-EM','Official curriculum Paper I',2,40),
('y3-em-5','bams_ncism_3','2021-22','AyUG-EM','y3-em-paper1','topic','5','Teevra Shwasa Vega: acute respiratory failure, status asthmaticus, ARDS and choking','NCISM AyUG-EM','Official curriculum Paper I',2,50),
('y3-em-6','bams_ncism_3','2021-22','AyUG-EM','y3-em-paper1','topic','6','Teevra Hikka','NCISM AyUG-EM','Official curriculum Paper I',2,60);