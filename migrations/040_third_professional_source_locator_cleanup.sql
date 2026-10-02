-- Source-quality correction for AyUG-SL topic 21.
-- The topic is part of the same official Table 2 Paper 1 source as its peers.
UPDATE curriculum_nodes
SET source_locator='Table 2 Paper 1'
WHERE curriculum_id='bams_ncism_3'
  AND subject_id='AyUG-SL'
  AND node_id='y3-sl-21';
