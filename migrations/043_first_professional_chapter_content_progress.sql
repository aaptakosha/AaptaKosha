-- NCISM first-professional content progress marker.
-- Chapter content is stored as static JSON; this migration only records its state
-- in the curriculum hierarchy without duplicating the lesson payload in SQLite.
UPDATE curriculum_nodes
SET status = 'content_in_progress'
WHERE curriculum_id = 'bams_ncism_1'
  AND curriculum_version = '2021-22'
  AND subject_id = 'AyUG-SA1'
  AND node_id = 'y1-sa1-2';

UPDATE curriculum_nodes SET status = 'content_in_progress'
WHERE curriculum_id = 'bams_ncism_1' AND curriculum_version = '2021-22'
  AND subject_id = 'AyUG-SA1' AND node_id = 'y1-sa1-3';
