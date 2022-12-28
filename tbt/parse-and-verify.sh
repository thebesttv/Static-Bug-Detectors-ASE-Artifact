#!/usr/bin/env bash

cd ../

GREEN="\x1B[0;32m"
BACK="\x1B[0m"

echo -e "${GREEN}> Parseing tool reports${BACK}"
bash scripts/parsers/run_parsers.sh

echo -e "${GREEN}> Verifying tool warnings${BACK}"
bash verify-scripts/run_verify_tool_warnings.sh

echo -e "${GREEN}> Creating and populating database tables (using reproduced warnings)${BACK}"
bash scripts/database/db_wrapper.sh -r -d study_db

echo -e "${GREEN}> Generating bug candidates via mapping methods${BACK}"
python3 scripts/database/run_mapping_methods.py study_db

echo -e "${GREEN}> Verifying bug candidates${BACK}"
python3 verify-scripts/verify_bug_candidates.py bug_candidates.json

echo -e "${GREEN}> Verifying true bugs${BACK}"
python3 verify-scripts/verify_true_bugs.py bug_candidates.json
