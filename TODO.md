# Refactoring TODO - Fake Job Detection Pipeline

## Step 1: ATS Trusted Domain Recognition

-   [x] Create `backend/app/constants/ats_constants.py` with TRUSTED_ATS_DOMAINS and helper
-   [x] Edit `backend/app/utils/url_utils.py` to add ATS URL helpers
-   [x] Edit `backend/app/agents/website_investigation_node.py` to detect ATS providers
-   [x] Edit `backend/app/agents/company_extraction_node.py` to recognize ATS domains
-   [x] Edit `backend/app/agents/evidence_aggregation_node.py` to pass ATS evidence
-   [x] Edit `backend/app/services/synthesis_service.py` to not flag missing career page for ATS

## Step 2: Neutralize Search Query Bias & Remove Artificial Multipliers

-   [x] Edit `backend/app/agents/common/tavily_utils.py` to neutralize search query
-   [x] Edit `backend/app/agents/common/gemini_analyzer.py` to use real evidence lengths

## Step 3: LLM Reasoning & Impersonation Handling

-   [x] Edit `backend/app/prompts/gemini_prompts.py` REASONING_PROMPT for entity resolution
-   [x] Edit `backend/app/agents/common/reputation_constants.py` REPUTATION_ANALYSIS_PROMPT for entity resolution

## Follow-up

-   [x] Verify all files <= 150 lines
-   [ ] Output manual commands in plain text
