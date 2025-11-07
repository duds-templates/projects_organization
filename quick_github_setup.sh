#!/bin/bash
# Quick GitHub Setup - Minimal Manual Steps Required
# This script does everything except org creation (web-only)

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║        QUICK GITHUB REORGANIZATION - AUTOMATED EXECUTION          ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

# Step 1: Check authentication
echo "Step 1: Checking GitHub CLI authentication..."
if ! gh auth status >/dev/null 2>&1; then
    echo -e "${RED}❌ Not authenticated${NC}"
    echo ""
    echo "MANUAL STEP REQUIRED:"
    echo "  1. Open a new terminal"
    echo "  2. Run: gh auth login"
    echo "  3. Choose: GitHub.com → HTTPS → Browser login"
    echo "  4. Authenticate in browser"
    echo "  5. Come back and run this script again"
    echo ""
    exit 1
fi

echo -e "${GREEN}✅ Authenticated${NC}"
gh auth status 2>&1 | grep "Logged in"
echo ""

# Step 2: Check for organizations
echo "Step 2: Checking if organizations exist..."
echo ""

ORGS_NEEDED=()

for org in duds-production duds-portfolio duds-templates; do
    if gh api "orgs/$org" >/dev/null 2>&1; then
        echo -e "${GREEN}✅ $org exists${NC}"
    else
        echo -e "${YELLOW}⚠️  $org not found${NC}"
        ORGS_NEEDED+=("$org")
    fi
done

if [ ${#ORGS_NEEDED[@]} -gt 0 ]; then
    echo ""
    echo -e "${YELLOW}MANUAL STEP REQUIRED:${NC}"
    echo "Organizations must be created via web interface (GitHub restriction)"
    echo ""
    echo "Quick links to create (takes 2 min each):"
    for org in "${ORGS_NEEDED[@]}"; do
        echo "  → https://github.com/account/organizations/new?plan=free"
        echo "    Organization name: $org"
        echo ""
    done
    echo "After creating organizations, run this script again."
    echo ""
    
    # Open browser to help
    echo "Opening browser..."
    open "https://github.com/account/organizations/new?plan=free" 2>/dev/null || \
        echo "Please visit: https://github.com/account/organizations/new?plan=free"
    echo ""
    exit 1
fi

echo -e "${GREEN}✅ All organizations exist!${NC}"
echo ""

# From here on, everything is automated
echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║                   AUTOMATED EXECUTION STARTING                     ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

# Now run the main setup script
cd /Users/dalerogers/Projects
./github_org_setup.sh

echo ""
echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║                         ✅ COMPLETE!                               ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""
echo "Next steps:"
echo "  1. Run: ./update_remotes.sh"
echo "  2. Run: ./verify_github_setup.sh"
echo "  3. Run: ./sync_projects.sh status"
echo ""

