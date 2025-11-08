#!/bin/bash
#
# Wrapper script to run DMARC parser with environment variables
# Usage: ./run_dmarc_parser.sh
#

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${SCRIPT_DIR}"

# Load environment variables if .env.dmarc exists
if [ -f ".env.dmarc" ]; then
    echo "Loading configuration from .env.dmarc..."
    export $(grep -v '^#' .env.dmarc | xargs)
else
    echo "Error: .env.dmarc file not found!"
    echo "Please copy .env.dmarc.example to .env.dmarc and configure it."
    exit 1
fi

# Check required variables
if [ -z "${GMAIL_EMAIL}" ] || [ -z "${GMAIL_APP_PASSWORD}" ]; then
    echo "Error: GMAIL_EMAIL and GMAIL_APP_PASSWORD must be set in .env.dmarc"
    exit 1
fi

# Set defaults
IMAP_SERVER=${IMAP_SERVER:-imap.gmail.com}
MAILBOX=${MAILBOX:-INBOX}
LIMIT=${LIMIT:-50}
OUTPUT_FILE=${OUTPUT_FILE:-dmarc_failures_$(date +%Y%m%d_%H%M%S).json}

echo "======================================"
echo "DMARC Report Parser"
echo "======================================"
echo "Email: ${GMAIL_EMAIL}"
echo "Server: ${IMAP_SERVER}"
echo "Mailbox: ${MAILBOX}"
echo "Limit: ${LIMIT}"
echo "Output: ${OUTPUT_FILE}"
echo "======================================"
echo ""

# Run the parser
python3 dmarc_parser.py \
  --email "${GMAIL_EMAIL}" \
  --password "${GMAIL_APP_PASSWORD}" \
  --server "${IMAP_SERVER}" \
  --mailbox "${MAILBOX}" \
  --limit "${LIMIT}" \
  --output "${OUTPUT_FILE}"

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    echo "Report saved successfully to: ${OUTPUT_FILE}"
else
    echo ""
    echo "Error: Script exited with code ${EXIT_CODE}"
fi

exit $EXIT_CODE
