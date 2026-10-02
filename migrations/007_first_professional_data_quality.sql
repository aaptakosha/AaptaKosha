
-- Correct NCISM row-spanned marks: the 26 marks belong to the grouped block,
-- not individually to topics 4-8.
UPDATE curriculum_nodes SET marks = NULL WHERE node_id IN
('y1-ks-4','y1-ks-5','y1-ks-6','y1-ks-7','y1-ks-8');
