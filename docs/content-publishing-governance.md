# AaptaKosha content publishing rule

## Universal rule: additive publishing only

Adding a new subject, chapter, unit, lesson, translation, diagram, or exam resource must be additive. A new content change must never delete, replace, or hide previously published content.

### Required publishing behavior
- Give every subject/chapter/unit a stable ID.
- Add new content with new IDs/files; do not reuse an existing published ID for a different chapter.
- Curriculum SQL must use additive statements such as `INSERT OR IGNORE` (SQLite) or `INSERT ... ON CONFLICT DO NOTHING`.
- Never use `DELETE`, `TRUNCATE`, `DROP TABLE`, or `REPLACE INTO` in curriculum migrations.
- Existing content must remain readable if a new migration fails.
- A failed new migration may be skipped after an atomic rollback; the previously published catalogue must remain available.
- Frontend pages must fail gracefully and must not convert an API error into an empty catalogue that looks like content was deleted.

## Deployment safety

SQLite curriculum migrations are executed atomically. The catalogue runner also isolates a failed migration so one bad chapter cannot take the complete curriculum offline.

The GitHub `Content preservation guard` blocks deletion/rename of files under `content/` and destructive curriculum SQL.

## Content generation workflow

1. Add the new chapter/content file.
2. Add an additive curriculum migration or stable content-registry entry.
3. Do not edit or remove older published content unless the change is a correction that preserves its stable ID and public availability.
4. Deploy.
5. Verify the new subject/chapter and at least one existing subject/chapter on the live site before continuing with the next content batch.

These rules apply to every future NCISM subject and chapter, not only Padartha Vijnanam.