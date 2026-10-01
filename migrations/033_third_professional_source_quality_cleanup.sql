-- Source-quality cleanup: remove only provisional SA3 chapter rows whose exact
-- official chapter table has not yet been re-verified.
DELETE FROM curriculum_nodes
WHERE node_id IN (
  'y3-sa3-samhita-charaka','y3-sa3-samhita-sushruta','y3-sa3-samhita-ashtanga',
  'y3-em-1'
);

DELETE FROM curriculum_nodes
WHERE node_id = 'y3-sa3-samhita';
