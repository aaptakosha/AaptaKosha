# AaptaKosha agent workflow

## Stitch MCP
When UI/design work is requested, use the configured Stitch MCP server when available.

- Treat Stitch as the design-generation and UI exploration layer.
- Preserve AaptaKosha's existing architecture, accessibility, responsive behavior, and NCISM-first product requirements.
- Do not replace existing production UI wholesale unless the task explicitly requests it.
- Prefer additive changes and a feature branch.
- Never commit Stitch API keys, OAuth tokens, or other credentials.
- Before merging Stitch-generated code, review it for consistency with the existing frontend and project conventions.

## Git workflow
- Work from a feature/setup branch rather than the main branch.
- Inspect current files before editing them.
- Do not delete or overwrite existing project assets without explicit approval.
- Run relevant tests and checks before proposing a merge.
