# Implementation Plan: Migrate existing Bootstrap-based CSS to Tailwind CSS

## Phase 1: Tailwind CSS Setup [checkpoint: 128393e]

- [x] Task: Install Tailwind CSS and dependencies 5ee5735
    - [x] Add Tailwind to project (via CDN or local build process)
    - [x] Create `tailwind.config.js` with evolved palette
- [x] Task: Configure Django for Tailwind 8f31032
    - [x] Update `base.html` to include Tailwind styles
    - [x] Verify Tailwind is loading correctly
- [x] Task: Conductor - User Manual Verification 'Tailwind CSS Setup' (Protocol in workflow.md) 128393e

## Phase 2: Base Template Migration [checkpoint: 5a7c7a1]

- [x] Task: Migrate Navbar to Tailwind f8aa195
    - [x] Replace Bootstrap navbar classes with Tailwind utilities
    - [x] Recreate "Pacifico" logo and SVG icon styling
- [x] Task: Migrate Main Container and Layout 07869f8
    - [x] Apply Tailwind layout utilities to `base.html` content block
- [x] Task: Conductor - User Manual Verification 'Base Template Migration' (Protocol in workflow.md) 5a7c7a1

## Phase 3: Meal List View Migration

- [~] Task: Write Tests for Meal List UI
    - [ ] Verify presence of key UI elements after migration
- [ ] Task: Migrate Meal Card Component
    - [ ] Replace Bootstrap card classes with Tailwind
    - [ ] Ensure 200x200 square image display is maintained
- [ ] Task: Migrate Filter Toolbar
    - [ ] Update `django-filter` form styling to Tailwind
- [ ] Task: Conductor - User Manual Verification 'Meal List View Migration' (Protocol in workflow.md)

## Phase 4: Detail, Forms & Cleanup

- [ ] Task: Migrate Meal Detail View
    - [ ] Update detail layout and badges to Tailwind
- [ ] Task: Migrate Meal Forms (Create/Update)
    - [ ] Apply Tailwind styling to form inputs and buttons
- [ ] Task: Final CSS Cleanup
    - [ ] Remove `meals.css` and Bootstrap links
    - [ ] Verify all Quality Gates (coverage, mobile, accessibility)
- [ ] Task: Conductor - User Manual Verification 'Detail, Forms & Cleanup' (Protocol in workflow.md)
