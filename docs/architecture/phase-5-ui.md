# Phase 5 — UI/UX Architecture

## Purpose
Phase 5 adds a replaceable presentation layer without coupling visual design to the Phase 1–4 domain and persistence contracts.

## Principles
- UI is a replaceable presentation layer.
- Existing curriculum, content, assessment and learner contracts remain the source of truth.
- Responsive layout is intrinsic to every screen.
- Design tokens and reusable components are centralized.
- Visual redesigns must not require database migrations unless product behavior changes.
- Accessibility and touch-friendly controls are first-class requirements.

## Responsive model
The frontend reflows across wide desktop, laptop, tablet landscape, tablet portrait, mobile and small mobile. Layouts use flexible grids, intrinsic sizing, minmax and clamp rather than duplicated device-specific pages.

## Current implementation
The frontend directory contains the first responsive visual implementation:
- index.html — semantic dashboard structure
- styles.css — design tokens, component styles and responsive rules
- app.js — minimal navigation and search interactions

This first slice is framework-neutral so the visual system can be validated before introducing a heavier client framework.

## Data boundary
The current dashboard uses representative display data. It does not redefine Phase 1–4 domain contracts. Future API integration should use DTO/view-model adapters rather than importing persistence models directly into UI components.

## Redesign strategy
A future redesign can replace colors, typography, spacing, component visuals, page composition and navigation presentation without changing learner, curriculum, content or assessment persistence structures.

## Acceptance direction
Every future screen should provide desktop, tablet and mobile layouts plus loading, empty and error states, keyboard/focus behavior and touch-friendly controls.
