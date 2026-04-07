# Spec Template

Copy for new features. Save as docs/plans/F-{id}-spec.md.

## Standard Spec

    # F-{id}: {Feature Name}
    ## Status: planned | in-progress | shipped | regressed | deprecated
    ## Why
    [What triggered this]
    ## What
    [One paragraph]
    ## Assumptions
    - [ ] {Assumption}
    ## Not Doing
    - {Excluded} -- {reason}
    ## Acceptance Criteria
    - [ ] {Criterion}
    ## Validation
    - Unit: {test or N/A}
    - E2E: {scenario or N/A}
    ## Tasks
    | ID | Desc | Pipeline | Depends | Status | Evidence |
    |----|------|----------|---------|--------|----------|
    | T1 | {task} | {agents} | -- | pending | |
    ### Running Notes
    #### T1
    - {date}: {notes}
    ## Files Affected
    - {path}: {changes}
    ## Status History
    - {date}: planned

## Minimal Spec (Bug Fixes)

    # B-{id}: {Description}
    ## Status: shipped
    ## Why
    [One-line symptom]
    ## Tasks
    | ID | Desc | Pipeline | Status | Evidence |
    |----|------|----------|--------|----------|
    | T1 | {fix} | {agent} | done | {output} |
