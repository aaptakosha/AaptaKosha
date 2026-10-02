-- Curriculum data-quality normalization after the verified third-professional topic loads.
-- Correct the provisional SA3 node-id gap without dropping the canonical topic row.
UPDATE curriculum_nodes
SET node_id='y3-sa3-17', code='17', sort_order=170
WHERE node_id='y3-sa3-18'
  AND curriculum_id='bams_ncism_3'
  AND subject_id='AyUG-SA3';