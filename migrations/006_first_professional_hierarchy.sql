

-- Additional first-professional source-verified structural anchors from NCISM Table 2.
INSERT OR IGNORE INTO curriculum_nodes
(node_id,curriculum_id,curriculum_version,subject_id,parent_node_id,node_type,code,name,source_reference,source_locator,term,marks,lecture_hours,non_lecture_hours,sort_order)
VALUES
('y1-rs-4','bams_ncism_1','2021-22','AyUG-RS','y1-rs-paper1','unit','4','Asthi Shaarira','NCISM AyUG-RS','Table 2, Paper I topic 4',1,4,2,1,40),
('y1-rs-5','bams_ncism_1','2021-22','AyUG-RS','y1-rs-paper1','unit','5','Sandhi Shaarira','NCISM AyUG-RS','Table 2, Paper I topic 5',2,4,2,3,50),
('y1-rs-6','bams_ncism_1','2021-22','AyUG-RS','y1-rs-paper1','unit','6','Snayu Sharir','NCISM AyUG-RS','Table 2, Paper I topic 6',2,3,2,1,60),
('y1-rs-7','bams_ncism_1','2021-22','AyUG-RS','y1-rs-paper1','unit','7','Peshi Shaarira','NCISM AyUG-RS','Table 2, Paper I topic 7',2,3,2,1,70),
('y1-rs-8','bams_ncism_1','2021-22','AyUG-RS','y1-rs-paper1','unit','8','Kesha, Danta, Nakha Sharir','NCISM AyUG-RS','Table 2, Paper I topic 8',2,4,2,1,80),
('y1-ks-4','bams_ncism_1','2021-22','AyUG-KS','y1-ks-paper1','unit','4','Vata Dosha','NCISM AyUG-KS','Table 2, Paper I topic 4',1,26,6,2,40),
('y1-ks-5','bams_ncism_1','2021-22','AyUG-KS','y1-ks-paper1','unit','5','Pitta Dosha','NCISM AyUG-KS','Table 2, Paper I topic 5',1,26,5,1,50),
('y1-ks-6','bams_ncism_1','2021-22','AyUG-KS','y1-ks-paper1','unit','6','Kapha Dosha','NCISM AyUG-KS','Table 2, Paper I topic 6',2,26,4,1,60),
('y1-ks-7','bams_ncism_1','2021-22','AyUG-KS','y1-ks-paper1','unit','7','Dosha Vriddhi-Kshaya','NCISM AyUG-KS','Table 2, Paper I topic 7',2,26,1,1,70),
('y1-ks-8','bams_ncism_1','2021-22','AyUG-KS','y1-ks-paper1','unit','8','Kriyakala','NCISM AyUG-KS','Table 2, Paper I topic 8',2,26,1,1,80),
('y1-ks-9','bams_ncism_1','2021-22','AyUG-KS','y1-ks-paper1','unit','9','Prakriti','NCISM AyUG-KS','Table 2, Paper I topic 9',2,7,7,3,90),
('y1-ks-10','bams_ncism_1','2021-22','AyUG-KS','y1-ks-paper1','unit','10','Ahara','NCISM AyUG-KS','Table 2, Paper I topic 10',3,3,3,1,100),
('y1-sa1-paper1','bams_ncism_1','2021-22','AyUG-SA1',NULL,'paper','I','Paper I','NCISM AyUG-SA1','Table 2: Contents of Course',NULL,NULL,NULL,NULL,10),
('y1-sa1-1','bams_ncism_1','2021-22','AyUG-SA1','y1-sa1-paper1','unit','1','Introduction to Samhita','NCISM AyUG-SA1','Table 2, topic 1',1,NULL,15,9,10),
('y1-sa1-2','bams_ncism_1','2021-22','AyUG-SA1','y1-sa1-paper1','chapter','AH.Su.1','Ayushkamiya Adhyaya','NCISM AyUG-SA1','Table 2, Ashtanga Hridaya Sutrasthana 1',1,50,8,3,20),
('y1-pv-paper2','bams_ncism_1','2021-22','AyUG-PV',NULL,'paper','II','Paper II','NCISM AyUG-PV','Table 2: Examination/Paper structure',NULL,NULL,NULL,NULL,20);
