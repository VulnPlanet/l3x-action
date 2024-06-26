import json
import os
from datetime import datetime

def process_results():
    with open('l3x_results.json', 'r') as f:
        results = json.load(f)

    comment = "## L3X Security Scan Results\n\n"
    sarif_results = []

    for vuln in results['vulnerabilities_details']:
        comment += f"### {vuln['title']} ({vuln['severity']})\n"
        comment += f"- **File:** {vuln['file']}\n"
        comment += f"- **Line:** {vuln['line_number']}\n"
        comment += f"- **Description:** {vuln['description']}\n"
        comment += f"- **Suggested Fix:** {vuln['fix']}\n\n"

        sarif_results.append({
            "ruleId": vuln['vulnerability_id'],
            "message": {
                "text": vuln['description']
            },
            "locations": [
                {
                    "physicalLocation": {
                        "artifactLocation": {
                            "uri": vuln['file']
                        },
                        "region": {
                            "startLine": vuln['line_number']
                        }
                    }
                }
            ],
            "partialFingerprints": {
                "primaryLocationLineHash": f"{vuln['file']}:{vuln['line_number']}"
            }
        })

    with open('/tmp/pr_comment.md', 'w') as f:
        f.write(comment)

    sarif_output = {
        "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
        "version": "2.1.0",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "L3X Security Scanner",
                        "informationUri": "https://github.com/VulnPlanet/l3x-action",
                        "rules": [
                            {
                                "id": vuln['vulnerability_id'],
                                "name": vuln['title'],
                                "shortDescription": {
                                    "text": vuln['title']
                                },
                                "fullDescription": {
                                    "text": vuln['description']
                                },
                                "helpUri": "https://vulnplanet.com/",
                                "help": {
                                    "text": f"Severity: {vuln['severity']}\nSuggested Fix: {vuln['fix']}"
                                }
                            } for vuln in results['vulnerabilities_details']
                        ]
                    }
                },
                "results": sarif_results
            }
        ]
    }

    with open('l3x_results.sarif', 'w') as f:
        json.dump(sarif_output, f)

if __name__ == "__main__":
    process_results()
