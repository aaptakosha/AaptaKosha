-- First-professional published-content wiring.
-- Additive only: preserve existing node IDs and update only incorrect legacy
-- codes/types so canonical content IDs remain stable.
BEGIN;

UPDATE curriculum_nodes SET code='AH.Su.2', node_type='chapter'
WHERE node_id='y1-sa1-3' AND subject_id='AyUG-SA1';
UPDATE curriculum_nodes SET code='AH.Su.3', node_type='chapter'
WHERE node_id='y1-sa1-4' AND subject_id='AyUG-SA1';
UPDATE curriculum_nodes SET code='AH.Su.4', node_type='chapter'
WHERE node_id='y1-sa1-5' AND subject_id='AyUG-SA1';
UPDATE curriculum_nodes SET code='AH.Su.5', node_type='chapter'
WHERE node_id='y1-sa1-6' AND subject_id='AyUG-SA1';
UPDATE curriculum_nodes SET code='AH.Su.6', node_type='chapter'
WHERE node_id='y1-sa1-7' AND subject_id='AyUG-SA1';
UPDATE curriculum_nodes SET code='AH.Su.7', node_type='chapter'
WHERE node_id='y1-sa1-8' AND subject_id='AyUG-SA1';
UPDATE curriculum_nodes SET code='AH.Su.8', node_type='chapter'
WHERE node_id='y1-sa1-9' AND subject_id='AyUG-SA1';
UPDATE curriculum_nodes SET code='AH.Su.9', node_type='chapter'
WHERE node_id='y1-sa1-10' AND subject_id='AyUG-SA1';
UPDATE curriculum_nodes SET code='AH.Su.10', node_type='chapter'
WHERE node_id='y1-sa1-11' AND subject_id='AyUG-SA1';
UPDATE curriculum_nodes SET code='AH.Su.11', node_type='chapter'
WHERE node_id='y1-sa1-12' AND subject_id='AyUG-SA1';
UPDATE curriculum_nodes SET code='AH.Su.12', node_type='chapter'
WHERE node_id='y1-sa1-13' AND subject_id='AyUG-SA1';
UPDATE curriculum_nodes SET code='AH.Su.13', node_type='chapter'
WHERE node_id='y1-sa1-14' AND subject_id='AyUG-SA1';
UPDATE curriculum_nodes SET code='AH.Su.14', node_type='chapter'
WHERE node_id='y1-sa1-15' AND subject_id='AyUG-SA1';
UPDATE curriculum_nodes SET code='AH.Su.15', node_type='chapter'
WHERE node_id='y1-sa1-16' AND subject_id='AyUG-SA1';

UPDATE curriculum_nodes SET code='Ch.Su.1', node_type='chapter'
WHERE node_id='y1-sa1-17' AND subject_id='AyUG-SA1';
UPDATE curriculum_nodes SET code='Ch.Su.2', node_type='chapter'
WHERE node_id='y1-sa1-18' AND subject_id='AyUG-SA1';
UPDATE curriculum_nodes SET code='Ch.Su.3', node_type='chapter'
WHERE node_id='y1-sa1-19' AND subject_id='AyUG-SA1';
UPDATE curriculum_nodes SET code='Ch.Su.4', node_type='chapter'
WHERE node_id='y1-sa1-20' AND subject_id='AyUG-SA1';
UPDATE curriculum_nodes SET code='Ch.Su.5', node_type='chapter'
WHERE node_id='y1-sa1-21' AND subject_id='AyUG-SA1';
UPDATE curriculum_nodes SET code='Ch.Su.6', node_type='chapter'
WHERE node_id='y1-sa1-22' AND subject_id='AyUG-SA1';
UPDATE curriculum_nodes SET code='Ch.Su.7', node_type='chapter'
WHERE node_id='y1-sa1-23' AND subject_id='AyUG-SA1';
UPDATE curriculum_nodes SET code='Ch.Su.8', node_type='chapter'
WHERE node_id='y1-sa1-24' AND subject_id='AyUG-SA1';
UPDATE curriculum_nodes SET code='Ch.Su.9', node_type='chapter'
WHERE node_id='y1-sa1-25' AND subject_id='AyUG-SA1';
UPDATE curriculum_nodes SET code='Ch.Su.10', node_type='chapter'
WHERE node_id='y1-sa1-26' AND subject_id='AyUG-SA1';
UPDATE curriculum_nodes SET code='Ch.Su.11', node_type='chapter'
WHERE node_id='y1-sa1-27' AND subject_id='AyUG-SA1';
UPDATE curriculum_nodes SET code='Ch.Su.12', node_type='chapter'
WHERE node_id='y1-sa1-28' AND subject_id='AyUG-SA1';

INSERT OR IGNORE INTO curriculum_nodes
(node_id,curriculum_id,curriculum_version,subject_id,parent_node_id,node_type,code,name,source_reference,source_locator,term,sort_order)
VALUES
('y1-snai1-1','bams_ncism_1','2021-22','AyUG-SN-AI','y1-sn-ai-paper1','unit','1','संस्कृतवर्णानाम् परिचयः','AaptaKosha published student content','content/sanskrit/01-varnamala-uccharana.md',1,10),
('y1-snai1-2','bams_ncism_1','2021-22','AyUG-SN-AI','y1-sn-ai-paper1','unit','2','संज्ञा-प्रकरणम्','AaptaKosha published student content','content/sanskrit/02-samjna-avyaya.md',1,20),
('y1-snai1-3','bams_ncism_1','2021-22','AyUG-SN-AI','y1-sn-ai-paper1','unit','3','शब्दरूप — सर्वनाम','AaptaKosha published student content','content/sanskrit/03-shabdarupa-sarvanama.md',1,30),
('y1-snai1-4','bams_ncism_1','2021-22','AyUG-SN-AI','y1-sn-ai-paper1','unit','4','धातुरूप','AaptaKosha published student content','content/sanskrit/04-dhaturupa.md',1,40),
('y1-snai1-5','bams_ncism_1','2021-22','AyUG-SN-AI','y1-sn-ai-paper1','unit','5','कारक-विभक्ति','AaptaKosha published student content','content/sanskrit/05-karaka-vibhakti.md',2,50),
('y1-snai1-6','bams_ncism_1','2021-22','AyUG-SN-AI','y1-sn-ai-paper1','unit','6','सन्धि','AaptaKosha published student content','content/sanskrit/06-sandhi.md',2,60),
('y1-snai1-7','bams_ncism_1','2021-22','AyUG-SN-AI','y1-sn-ai-paper1','unit','7','समास-प्रकरणम्','AaptaKosha published student content','content/sanskrit/07-samasa.md',2,70),
('y1-snai1-8','bams_ncism_1','2021-22','AyUG-SN-AI','y1-sn-ai-paper1','unit','8','उपसर्ग-प्रत्यय','AaptaKosha published student content','content/sanskrit/08-upasarga-pratyaya.md',2,80),
('y1-snai1-9','bams_ncism_1','2021-22','AyUG-SN-AI','y1-sn-ai-paper1','unit','9','पर्याय-निरुक्ति-कोश','AaptaKosha published student content','content/sanskrit/09-paryaya-nirukti-kosha.md',3,90),
('y1-snai1-10','bams_ncism_1','2021-22','AyUG-SN-AI','y1-sn-ai-paper1','unit','10','छन्द-अलंकार एवं text reading','AaptaKosha published student content','content/sanskrit/10-chandas-alankara-text-reading.md',3,100),
('y1-snai1-11','bams_ncism_1','2021-22','AyUG-SN-AI','y1-sn-ai-paper1','unit','11','आयुर्वेद अनुवाद-पद्धति एवं revision','AaptaKosha published student content','content/sanskrit/11-ayurveda-translation-method.md',3,110),
('y1-snai2-a1','bams_ncism_1','2021-22','AyUG-SN-AI','y1-snai2-a','unit','1','निरुक्ति तथा पर्यायपदानि','AaptaKosha published student content','content/sanskrit/paper-2/part-a/01-nirukti-paryaya.md',1,10),
('y1-snai2-a2','bams_ncism_1','2021-22','AyUG-SN-AI','y1-snai2-a','unit','2','परिभाषापदानि','AaptaKosha published student content','content/sanskrit/paper-2/part-a/02-paribhasha.md',1,20),
('y1-snai2-a3','bams_ncism_1','2021-22','AyUG-SN-AI','y1-snai2-a','unit','3','अष्टाङ्गहृदयम् — prescribed selected chapters','AaptaKosha published student content','content/sanskrit/paper-2/part-a/03-ashtanga-hridaya.md',2,30),
('y1-snai2-a4','bams_ncism_1','2021-22','AyUG-SN-AI','y1-snai2-a','unit','4','आयुर्वेद सुभाषित','AaptaKosha published student content','content/sanskrit/paper-2/part-a/04-ayurveda-subhashita.md',2,40),
('y1-snai2-a5','bams_ncism_1','2021-22','AyUG-SN-AI','y1-snai2-a','unit','5','पञ्चतन्त्रम् — prescribed stories','AaptaKosha published student content','content/sanskrit/paper-2/part-a/05-panchatantra.md',2,50);

COMMIT;
