# Bug Fix Plan - COMPLETED ✅

## Verified Bugs (12 real bugs after re-analysis)

| #   | Status | File(s)                                                                                                   | Fix                                                      |
| --- | ------ | --------------------------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| 2   | ✅     | `evidence_aggregation_node.py`                                                                            | Add all rich reputation analysis fields to evidence dict |
| 3   | ✅     | `verification_service.py`                                                                                 | Wrap ML pipeline in `run_in_executor`                    |
| 4   | ✅     | `text_utils.py`, `company_extraction_node.py`, `gemini_reasoning_node.py`, `gemini_analyzer.py`           | Create shared `parse_json_response()` utility            |
| 5   | ✅     | `keyword_detector.py`                                                                                     | Return original keywords, not escaped regex              |
| 6   | ✅     | `whois_investigation_node.py`, `website_investigation_node.py`, `online_reputation_investigation_node.py` | Append errors to global errors list                      |
| 7   | ✅     | `api/routes/verify.py`                                                                                    | Pass timestamp from service result to response           |
| 8   | ✅     | `graph.py`, `verification_service.py`, `synthesis_service.py`                                             | Centralize `agent_risk_score` default to graph.py only   |
| 9   | ✅     | `reddit_investigation_node.py`                                                                            | Delete orphan file                                       |
| 10  | ✅     | `pipeline.py`                                                                                             | Set fallback confidence to 0.5 instead of 0.0            |
| 11  | ✅     | `schemas/verification.py`, `api/routes/history.py`                                                        | Add pagination fields to response schema                 |
| 12  | ✅     | `config/settings.py`                                                                                      | Add `TAVILY_API_KEY` to startup validation               |
| 13  | ✅     | `classifier.py`                                                                                           | Add log warning when creating untrained model            |

## Summary of Changes

### Bug #2 - Evidence aggregation data loss

-   **File**: `backend/app/agents/evidence_aggregation_node.py`
-   **Fix**: Added `risk_score`, `overall_sentiment`, `legitimate_presence`, `scam_reports_found`, `confidence`, `summary`, `reasoning`, `key_findings`, `positive_mentions`, and `sentiment` to the online_reputation evidence block

### Bug #3 - Sync ML pipeline blocks async event loop

-   **File**: `backend/app/services/verification_service.py`
-   **Fix**: Wrapped `self.ml_pipeline.analyze(job_description)` in `await loop.run_in_executor(None, ...)` to prevent event loop blocking

### Bug #4 - JSON parsing scattered across files

-   **File**: `backend/app/utils/text_utils.py`
-   **Fix**: Created `parse_json_response()` utility that strips markdown fences, handles edge cases, and returns None on failure (no exceptions)
-   **Updated consumers**: `company_extraction_node.py`, `gemini_reasoning_node.py`, `gemini_analyzer.py` all use the shared utility

### Bug #5 - Keywords returned as escaped regex patterns

-   **File**: `backend/app/ml/keyword_detector.py`
-   **Fix**: Added `_pattern_to_keyword` mapping and used it in `detect_keywords()` to return original human-readable keywords

### Bug #6 - Error accumulation not tracked

-   **Files**: `backend/app/agents/whois_investigation_node.py`, `website_investigation_node.py`, `online_reputation_investigation_node.py`
-   **Fix**: Each node now appends failures to `updated_state["errors"]` with context (e.g., "WHOIS investigation failed: {error}")

### Bug #7 - Missing timestamp in verification response

-   **File**: `backend/app/api/routes/verify.py`
-   **Fix**: Route now passes `timestamp=result["timestamp"]` to `VerificationResponse`

### Bug #8 - Redundant agent_score None-checks

-   **File**: `backend/app/services/synthesis_service.py` (removed redundant None check), `verification_service.py` (uses `.get("agent_risk_score", 0.5)` instead of conditional)
-   **Centralized default**: `graph.py` already defaults to 0.5 in `run_agent_pipeline()`

### Bug #9 - Orphan file remains

-   **File**: `backend/app/agents/reddit_investigation_node.py` - **DELETED**
-   **Note**: This was dead code - stores results under `reddit_data`, not `online_reputation_data`, so was never consumed

### Bug #10 - Fallback confidence too low

-   **File**: `backend/app/ml/pipeline.py`
-   **Fix**: When `model_status == "fallback"`, confidence is set to `0.5` (moderate) instead of calculated from neutral probability

### Bug #11 - Pagination metadata missing from response

-   **Files**: `backend/app/schemas/verification.py`, `backend/app/api/routes/history.py`
-   **Fix**: Added `page`, `limit`, `total_pages` fields to `VerificationHistoryResponse` schema; route passes them through

### Bug #12 - TAVILY_API_KEY not validated on startup

-   **File**: `backend/app/config/settings.py`
-   **Fix**: Added `"TAVILY_API_KEY": self.tavily_api_key` to the `validate_required_variables()` required set

### Bug #13 - Silent model creation misleads operators

-   **File**: `backend/app/ml/classifier.py`
-   **Fix**: Added explicit `logger.warning()` when no saved model is found, explaining the fallback behavior
