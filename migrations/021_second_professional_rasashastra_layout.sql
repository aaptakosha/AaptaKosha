DELETE FROM curriculum_nodes WHERE node_id IN ('y2-rb-1','y2-rb-2');

INSERT OR IGNORE INTO curriculum_nodes
(node_id,curriculum_id,curriculum_version,subject_id,parent_node_id,node_type,code,name,source_reference,source_locator,term,marks,sort_order)
VALUES
('y2-rb1-1','bams_ncism_2','2021-22','AyUG-RB','y2-rb-paper1','unit','1','Chronological development of Ayurvediya Aushadhi Nirmana','NCISM AyUG-RB','Table 6-F Paper 1',1,5,10),
('y2-rb1-2','bams_ncism_2','2021-22','AyUG-RB','y2-rb-paper1','unit','2','Paribhasha (Terminology)','NCISM AyUG-RB','Table 6-F Paper 1',1,10,20),
('y2-rb1-3','bams_ncism_2','2021-22','AyUG-RB','y2-rb-paper1','unit','3','Adharbhuta Siddhanta (Application of fundamental principles)','NCISM AyUG-RB','Table 6-F Paper 1',1,5,30),
('y2-rb1-4','bams_ncism_2','2021-22','AyUG-RB','y2-rb-paper1','unit','4','Yantropakaranani-I (Equipments and machineries)','NCISM AyUG-RB','Table 6-F Paper 1',1,5,40),
('y2-rb1-5','bams_ncism_2','2021-22','AyUG-RB','y2-rb-paper1','unit','5','Yantropakaranani-II (Equipments, fuel and Heating Devices)','NCISM AyUG-RB','Table 6-F Paper 1',1,5,50),
('y2-rb1-6','bams_ncism_2','2021-22','AyUG-RB','y2-rb-paper1','unit','6','Kalpana Nirmana I (Primary & Secondary dosage forms)','NCISM AyUG-RB','Table 6-F Paper 1',1,10,60),
('y2-rb1-7','bams_ncism_2','2021-22','AyUG-RB','y2-rb-paper1','unit','7','Kalpana Nirmana-II (Method of Preparation of different dosage forms & Dietary Supplements)','NCISM AyUG-RB','Table 6-F Paper 1',1,10,70),
('y2-rb1-8','bams_ncism_2','2021-22','AyUG-RB','y2-rb-paper1','unit','8','Rasa Dravya Parichaya-I','NCISM AyUG-RB','Table 6-F Paper 1',2,10,80),
('y2-rb1-9','bams_ncism_2','2021-22','AyUG-RB','y2-rb-paper1','unit','9','Rasa Dravya Parichaya-II','NCISM AyUG-RB','Table 6-F Paper 1',2,5,90),
('y2-rb1-10','bams_ncism_2','2021-22','AyUG-RB','y2-rb-paper1','unit','10','Rasadravya Parichaya-III','NCISM AyUG-RB','Table 6-F Paper 1',2,5,100),
('y2-rb1-11','bams_ncism_2','2021-22','AyUG-RB','y2-rb-paper1','unit','11','Kalpana Nirman-III (Method of Preparation of different dosage forms)','NCISM AyUG-RB','Table 6-F Paper 1',2,10,110),
('y2-rb1-12','bams_ncism_2','2021-22','AyUG-RB','y2-rb-paper1','unit','12','Chaturvidha Rasayana','NCISM AyUG-RB','Table 6-F Paper 1',2,10,120),
('y2-rb1-13','bams_ncism_2','2021-22','AyUG-RB','y2-rb-paper1','unit','13','Current and emerging trend in Ayurvedic pharmaceuticals','NCISM AyUG-RB','Table 6-F Paper 1',3,5,130),
('y2-rb1-14','bams_ncism_2','2021-22','AyUG-RB','y2-rb-paper1','unit','14','GMP (Schedule T) & Regulatory aspects of Ayurvedic drugs','NCISM AyUG-RB','Table 6-F Paper 1',3,5,140),
('y2-rb2-1','bams_ncism_2','2021-22','AyUG-RB','y2-rb-paper2','unit','1','Aushadhi Prayoga Vigyana','NCISM AyUG-RB','Table 6-F Paper 2',1,5,10),
('y2-rb2-2','bams_ncism_2','2021-22','AyUG-RB','y2-rb-paper2','unit','2','Single drug (Herbal & Mineral)','NCISM AyUG-RB','Table 6-F Paper 2',1,10,20),
('y2-rb2-3','bams_ncism_2','2021-22','AyUG-RB','y2-rb-paper2','unit','3','Single drug (Bhasma, Shuddha & Pishti)','NCISM AyUG-RB','Table 6-F Paper 2',2,15,30),
('y2-rb2-4','bams_ncism_2','2021-22','AyUG-RB','y2-rb-paper2','unit','4','Aushadhi Kalpa-I (Compound formulations)','NCISM AyUG-RB','Table 6-F Paper 2',2,15,40),
('y2-rb2-5','bams_ncism_2','2021-22','AyUG-RB','y2-rb-paper2','unit','5','Aushadhi Kalpa-II (Compound Drugs/Formulations)','NCISM AyUG-RB','Table 6-F Paper 2',3,15,50),
('y2-rb2-6','bams_ncism_2','2021-22','AyUG-RB','y2-rb-paper2','unit','6','Dosage Forms & Cosmetic Products','NCISM AyUG-RB','Table 6-F Paper 2',3,5,60),
('y2-rb2-7','bams_ncism_2','2021-22','AyUG-RB','y2-rb-paper2','unit','7','Nutraceuticals','NCISM AyUG-RB','Table 6-F Paper 2',3,5,70),
('y2-rb2-8','bams_ncism_2','2021-22','AyUG-RB','y2-rb-paper2','unit','8','Anupana Prayoga for Aushadhi Kalpa','NCISM AyUG-RB','Table 6-F Paper 2',3,5,80),
('y2-rb2-9','bams_ncism_2','2021-22','AyUG-RB','y2-rb-paper2','unit','9','Aushadhi Prayoga Marga','NCISM AyUG-RB','Table 6-F Paper 2',3,10,90),
('y2-rb2-10','bams_ncism_2','2021-22','AyUG-RB','y2-rb-paper2','unit','10','Rational prescription along with safe dispensing of Ayurvedic formulations','NCISM AyUG-RB','Table 6-F Paper 2',3,5,100),
('y2-rb2-11','bams_ncism_2','2021-22','AyUG-RB','y2-rb-paper2','unit','11','Traditional & Local health Practices','NCISM AyUG-RB','Table 6-F Paper 2',3,5,110),
('y2-rb2-12','bams_ncism_2','2021-22','AyUG-RB','y2-rb-paper2','unit','12','Pharmacovigilance for Ayurveda drugs','NCISM AyUG-RB','Table 6-F Paper 2',3,5,120);