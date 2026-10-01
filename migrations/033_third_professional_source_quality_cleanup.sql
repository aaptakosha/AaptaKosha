-- Source-quality cleanup: remove provisional topic/chapter rows where exact official
-- table extraction has not been re-verified. Keep the verified subject/paper shells.
DELETE FROM curriculum_nodes
WHERE node_id IN (
  'y3-em-1','y3-em-2','y3-em-3','y3-em-4','y3-em-5','y3-em-6',
  'y3-sa3-samhita-charaka','y3-sa3-samhita-sushruta','y3-sa3-samhita-ashtanga'
);

DELETE FROM curriculum_nodes
WHERE node_id = 'y3-sa3-samhita';