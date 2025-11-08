#!/bin/bash
#
# Jenkins Job Script for DMARC Parser
# 
# This script should be added as a "Execute shell" build step in Jenkins
#
# Prerequisites:
# 1. Add credentials in Jenkins (Manage Jenkins -> Manage Credentials):
#    - GMAIL_EMAIL (Secret text)
#    - GMAIL_APP_PASSWORD (Secret text)
# 2. Install Python 3.7+ on Jenkins server
# 3. Create reports directory: mkdir -p /var/jenkins_home/dmarc_reports
#

set -e  # Exit on error

# Configuration
SCRIPT_DIR="/var/jenkins_home/scripts"  # Adjust to your path
REPORT_DIR="/var/jenkins_home/dmarc_reports"  # Adjust to your path
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
REPORT_FILE="${REPORT_DIR}/dmarc_failures_${TIMESTAMP}.json"

# Ensure directories exist
mkdir -p "${REPORT_DIR}"

# Change to script directory
cd "${SCRIPT_DIR}"

echo "======================================"
echo "DMARC Report Parser - Jenkins Job"
echo "Started at: $(date)"
echo "======================================"
echo ""

# Run DMARC parser
python3 dmarc_parser.py \
  --email "${GMAIL_EMAIL}" \
  --password "${GMAIL_APP_PASSWORD}" \
  --limit 100 \
  --output "${REPORT_FILE}"

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    echo "SUCCESS: DMARC parser completed successfully"
    echo "Report saved to: ${REPORT_FILE}"
    
    # Check if failures were found
    FAILURE_COUNT=$(python3 -c "import json; data=json.load(open('${REPORT_FILE}')); print(data['total_failures'])")
    
    if [ "$FAILURE_COUNT" -gt 0 ]; then
        echo ""
        echo "WARNING: ${FAILURE_COUNT} DMARC failures detected!"
        echo "Please review the report: ${REPORT_FILE}"
        
        # Optional: Send email alert
        # mail -s "DMARC Failures Detected: ${FAILURE_COUNT}" admin@yourdomain.com < "${REPORT_FILE}"
        
        # Optional: Trigger another Jenkins job
        # curl -X POST http://jenkins-server/job/DMARC-Alert/build
    else
        echo ""
        echo "All DMARC checks passed - no failures found"
    fi
    
    # Cleanup old reports (keep last 30 days)
    find "${REPORT_DIR}" -name "dmarc_failures_*.json" -mtime +30 -delete
    
else
    echo ""
    echo "ERROR: DMARC parser failed with exit code ${EXIT_CODE}"
    exit ${EXIT_CODE}
fi

echo ""
echo "Completed at: $(date)"
echo "======================================"
