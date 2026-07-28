# Online Reputation Refactor - TODO

## Completed Steps

-   [x] Phase 1: Complete codebase analysis completed

## Phase 2 — File Rename

-   [x] Rename `reddit_investigation_node.py` → `online_reputation_investigation_node.py`

## Phase 3 — Backend Code Changes

-   [x] Update `online_reputation_investigation_node.py` (rename internal vars, comments, docstrings)
-   [x] Update `agent_state.py` (field name `reddit_data` → `online_reputation_data`)
-   [x] Update `graph.py` (import alias, node name, edges, state field)
-   [x] Update `evidence_aggregation_node.py` (vars, evidence keys, comments)
-   [x] Update `gemini_reasoning_node.py` (vars, prompt format)
-   [x] Update `synthesis_service.py` (vars, error messages)
-   [x] Update `gemini_prompts.py` (placeholder, comments)
-   [x] Update `custom_exceptions.py` (docstring)

## Phase 4 — Documentation

-   [x] Update `README.md` (remove Reddit references, env vars, PRAW)
-   [x] Update `ARCHITECTURE_PLAN.md` (folder structure, pipeline desc)
-   [x] Update `requirements.md` (remove PRAW reference)

## Phase 5 — Frontend Changes

-   [x] Update `EvidenceList.jsx` (labels, evidence key)
-   [x] Update `LoadingProgress.jsx` (step label)

## Phase 6 — Internal Validation

-   [x] Verify all changes are consistent and complete
-   [x] No syntax/import errors
-   [x] No broken references
