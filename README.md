# L3X

This action runs the L3X AI-driven Static Analyzer on your codebase.

## Features

- Scans Rust and Solidity code for vulnerabilities
- Validates findings using ChatGPT (optional)
- Posts scan results as comments on Pull Requests
- Uploads results to GitHub's Security page

## Usage

```yaml
name: L3X AI-driven Static Analyzer

on: [push, pull_request]

jobs:
  security_scan:
    runs-on: ubuntu-latest
    permissions:
      security-events: write
    steps:
    - uses: actions/checkout@v2
    - name: Run L3X Security Scanner
      uses: VulnPlanet/l3x-action@v1
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        openai_api_key: ${{ secrets.OPENAI_API_KEY }}
        validate_all_severities: 'true'
        model: 'gpt-3.5-turbo'
```
