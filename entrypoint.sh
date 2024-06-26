#!/bin/bash
set -e

/l3x/target/release/l3x "$GITHUB_WORKSPACE" \
  ${INPUT_OPENAI_API_KEY:+--openai-api-key "$INPUT_OPENAI_API_KEY"} \
  ${INPUT_OPENAI_ORG_ID:+--openai-org-id "$INPUT_OPENAI_ORG_ID"} \
  ${INPUT_OPENAI_PROJECT_ID:+--openai-project-id "$INPUT_OPENAI_PROJECT_ID"} \
  ${INPUT_VALIDATE_ALL_SEVERITIES:+--all-severities} \
  --model "$INPUT_MODEL" \
  ${INPUT_NO_VALIDATION:+--no-validation}

python3 /l3x/process_results.py

if [ "$GITHUB_EVENT_NAME" == "pull_request" ]; then
  COMMENT_BODY=$(cat /tmp/pr_comment.md)
  PR_NUMBER=$(jq -r ".pull_request.number" "$GITHUB_EVENT_PATH")
  REPO_FULLNAME=$(jq -r ".repository.full_name" "$GITHUB_EVENT_PATH")
  curl -s -S -H "Authorization: token $INPUT_GITHUB_TOKEN" \
       -X POST -d "{\"body\":\"$COMMENT_BODY\"}" \
       "https://api.github.com/repos/$REPO_FULLNAME/issues/$PR_NUMBER/comments"
fi

if [ -f "l3x_results.sarif" ]; then
  echo "Uploading SARIF file"
  curl -s -S -H "Authorization: token $INPUT_GITHUB_TOKEN" \
       -H "Accept: application/vnd.github.v3+json" \
       -X POST -F "sarif=@l3x_results.sarif" \
       "https://api.github.com/repos/$GITHUB_REPOSITORY/code-scanning/sarifs"
fi
