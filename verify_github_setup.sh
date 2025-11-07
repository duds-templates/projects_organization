#!/bin/bash
# Verify GitHub Organizations and Repository Setup

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo "======================================================================="
echo "GITHUB SETUP VERIFICATION"
echo "======================================================================="
echo ""

# Check authentication
echo "🔐 Checking Authentication..."
if gh auth status >/dev/null 2>&1; then
    echo -e "${GREEN}✅ GitHub CLI authenticated${NC}"
    gh auth status 2>&1 | grep "Logged in to"
else
    echo -e "${RED}❌ Not authenticated${NC}"
    echo "Run: gh auth login"
    exit 1
fi
echo ""

# Check organizations
echo "🏢 Checking Organizations..."
ORGS=("duds-production" "duds-portfolio" "duds-templates")

for org in "${ORGS[@]}"; do
    if gh api "orgs/$org" >/dev/null 2>&1; then
        repo_count=$(gh repo list "$org" --limit 100 --json name --jq '. | length')
        echo -e "${GREEN}✅ $org exists ($repo_count repos)${NC}"
        gh repo list "$org" --limit 10 --json name,url --jq '.[] | "   • \(.name): \(.url)"'
    else
        echo -e "${YELLOW}⚠️  $org not found - needs to be created${NC}"
    fi
    echo ""
done

# Check expected repositories
echo "📦 Checking Expected Repositories..."

check_repo() {
    local repo=$1
    if gh repo view "$repo" >/dev/null 2>&1; then
        echo -e "${GREEN}✅ $repo${NC}"
        return 0
    else
        echo -e "${RED}❌ $repo (not found)${NC}"
        return 1
    fi
}

echo ""
echo "Production:"
check_repo "duds-production/aegrid"

echo ""
echo "Portfolio:"
check_repo "duds-portfolio/dale_rogers_portfolio"
check_repo "duds-portfolio/portfolio_v3"
check_repo "duds-portfolio/portfolio"

echo ""
echo "Templates:"
check_repo "duds-templates/cursor_rules_library"
check_repo "duds-templates/project_templates"

echo ""
echo "Personal (Experimental):"
check_repo "Duds/procedural_design_scratch"
check_repo "Duds/bid_writer"
check_repo "Duds/bid_writer_mvp"
check_repo "Duds/my_nab"

echo ""
echo "======================================================================="
echo "VERIFICATION COMPLETE"
echo "======================================================================="

