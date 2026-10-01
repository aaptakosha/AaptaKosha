-- Curriculum data-quality normalization after the verified third-professional topic loads.
-- Keep stable topic codes while correcting an accidental node-id gap in SA3.
DELETE FROM curriculum_nodes
WHERE node_id='y3-sa3-18'
  AND curriculum_id='bams_ncism_3'
  AND subject_id='AyUG-SA3';

INSERT OR IGNORE INTO curriculum_nodes
(node_id,curriculum_id,curriculum_version,subject_id,parent_node_id,node_type,code,name,source_reference,source_locator,term,marks,lecture_hours,non_lecture_hours,sort_order)
SELECT
  'y3-sa3-17',curriculum_id,curriculum_version,subject_id,parent_node_id,node_type,code,name,source_reference,source_locator,term,marks,lecture_hours,non_lecture_hours,170
FROM curriculum_nodes
WHERE curriculum_id='bams_ncism_3'
  AND subject_id='AyUG-SA3'
  AND code='17';
