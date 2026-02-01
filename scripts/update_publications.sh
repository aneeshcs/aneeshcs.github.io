#!/bin/bash
#
# Publication Update Script
# Updates publications from BibTeX file using the academic CLI
#
# Usage: ./scripts/update_publications.sh [path_to_bibfile]
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Publication Update Script ===${NC}"
echo ""

# Check if academic CLI is installed
if ! command -v academic &> /dev/null; then
    echo -e "${YELLOW}Academic CLI not found. Installing...${NC}"
    pip install -U academic
fi

# Find BibTeX file
if [ -n "$1" ]; then
    BIB_FILE="$1"
elif [ -f "publication/ReadCube_export.bib" ]; then
    BIB_FILE="publication/ReadCube_export.bib"
else
    BIB_FILE=$(find publication -name "*.bib" | head -1)
fi

if [ -z "$BIB_FILE" ] || [ ! -f "$BIB_FILE" ]; then
    echo -e "${RED}Error: No BibTeX file found!${NC}"
    echo "Usage: $0 [path_to_bibfile]"
    echo "Or place a .bib file in the publication/ directory"
    exit 1
fi

echo -e "Using BibTeX file: ${GREEN}$BIB_FILE${NC}"
echo ""

# Import publications
echo -e "${YELLOW}Importing publications...${NC}"
academic import --bibtex "$BIB_FILE" --publication-dir content/publication/

echo ""
echo -e "${GREEN}Done! Publications imported to content/publication/${NC}"
echo "Run 'hugo server' to preview the changes."
