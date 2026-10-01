-- Correct the earlier Kriya Paper II seed in place: topics 1-16 are Ayurveda/Kriya theory;
-- contemporary physiology is the separate Part-B sequence 1-8.
-- In-place correction preserves any future references to the existing node IDs.
UPDATE curriculum_nodes SET code='B1', name='Haemopoetic system', source_locator='Paper II Part-B topic 1', term=1, sort_order=101 WHERE node_id='y1-ks2-17';
UPDATE curriculum_nodes SET code='B2', name='Immunity', source_locator='Paper II Part-B topic 2', term=1, sort_order=102 WHERE node_id='y1-ks2-18';
UPDATE curriculum_nodes SET code='B3', name='Physiology of cardio-vascular system', source_locator='Paper II Part-B topic 3', term=1, sort_order=103 WHERE node_id='y1-ks2-19';
UPDATE curriculum_nodes SET code='B4', name='Muscle physiology', source_locator='Paper II Part-B topic 4', term=2, sort_order=104 WHERE node_id='y1-ks2-20';
UPDATE curriculum_nodes SET code='B5', name='Adipose tissue', source_locator='Paper II Part-B topic 5', term=2, sort_order=105 WHERE node_id='y1-ks2-21';
UPDATE curriculum_nodes SET code='B6', name='Physiology of male and female reproductive systems', source_locator='Paper II Part-B topic 6', term=2, sort_order=106 WHERE node_id='y1-ks2-22';
UPDATE curriculum_nodes SET code='B7', name='Physiology of Excretion', source_locator='Paper II Part-B topic 7', term=3, sort_order=107 WHERE node_id='y1-ks2-23';
UPDATE curriculum_nodes SET code='B8', name='Special Senses, Sleep and Dreams', source_locator='Paper II Part-B topic 8', term=3, sort_order=108 WHERE node_id='y1-ks2-24';