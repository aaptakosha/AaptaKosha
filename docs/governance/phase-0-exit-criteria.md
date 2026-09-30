# Phase 0 Exit Criteria

Phase 0 can transition to Phase 1 when each gate has recorded evidence.

| Gate | Requirement | State |
|---|---|---|
| G0.1 | Project scope and extensibility defined | Complete |
| G0.2 | NCISM is the academic source backbone | Complete |
| G0.3 | Initial database/schema blueprint exists | Complete |
| G0.4 | Connector/delegation strategy established | Complete |
| G0.5 | Central project tracker exists | Complete |
| G0.6 | Authoritative NCISM source registry frozen | Ongoing |
| G0.7 | Implementation baseline versioned | Complete |
| G0.8 | Curriculum ingestion model mapped | Complete |
| G0.9 | Automation/reconciliation design defined | Complete |
| G0.10 | Phase 0 readiness review recorded | Pending |

The repository is not considered Phase 0 complete until G0.6 and G0.10 are evidenced in version control and the project tracker.

## G0.9 evidence

- Automation and reconciliation lifecycle is defined in `docs/automation/ncism-reconciliation-v0.1.md`.
- The design covers source discovery, fingerprinting, capture, parsing, normalization, comparison, change classification, validation, review routing, publication, audit, failure recovery, and supersession.
- Phase 1 implementation targets are explicitly separated from the Phase 0 design baseline.

## Phase 0 readiness review

Before Phase 1 begins, record:
1. final verification of all authoritative NCISM source entries;
2. tracker synchronization;
3. confirmation that G0.1-G0.9 evidence is versioned;
4. confirmation that no unresolved Phase 0 blocker remains;
5. approval to start Phase 1 implementation.
