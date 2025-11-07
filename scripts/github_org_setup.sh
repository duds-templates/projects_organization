#!/bin/bash
# GitHub Organization Setup and Repository Renaming Script
# This script renames and transfers repositories to organizations

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo "======================================================================="
echo "GITHUB ORGANIZATION SETUP"
echo "======================================================================="
echo ""

# Check GitHub CLI authentication
echo "🔐 Checking GitHub CLI authentication..."
if ! gh auth status >/dev/null 2>&1; then
    echo -e "${RED}❌ GitHub CLI not authenticated${NC}"
    echo ""
    echo "Please run: gh auth login"
    echo ""
    exit 1
fi

echo -e "${GREEN}✅ GitHub CLI authenticated${NC}"
echo ""

# Step 1: Check if organizations exist
echo "📋 Step 1: Checking if organizations exist..."
echo ""

ORGS=("duds-production" "duds-portfolio" "duds-templates")
ORGS_EXIST=true

for org in "${ORGS[@]}"; do
    if gh api "orgs/$org" >/dev/null 2>&1; then
        echo -e "${GREEN}✅ Organization exists: $org${NC}"
    else
        echo -e "${YELLOW}⚠️  Organization not found: $org${NC}"
        ORGS_EXIST=false
    fi
done

if [ "$ORGS_EXIST" = false ]; then
    echo ""
    echo -e "${YELLOW}⚠️  Some organizations don't exist yet${NC}"
    echo ""
    echo "Please create organizations manually:"
    echo "1. Go to: https://github.com/organizations/plan"
    echo "2. Create these organizations (Free tier):"
    echo "   - duds-production"
    echo "   - duds-portfolio"
    echo "   - duds-templates"
    echo ""
    echo "After creating organizations, run this script again."
    echo ""
    exit 1
fi

echo ""
echo "======================================================================="
echo "Step 2: Renaming Repositories"
echo "======================================================================="
echo ""

# Rename repositories (must happen before transfer)
declare -A RENAMES=(
    ["Duds/Aegrid"]="aegrid"
    ["Duds/dale-rogers-portfolio"]="dale_rogers_portfolio"
    ["Duds/portfolio-v3"]="portfolio_v3"
    ["Duds/procedural-design-scratch"]="procedural_design_scratch"
    ["Duds/BidWriter"]="bid_writer"
    ["Duds/BidWriter_MVP"]="bid_writer_mvp"
    ["Duds/MyNAB"]="my_nab"
    ["Duds/GoogleDocsScripts"]="google_docs_scripts"
    ["Duds/CriticalView360"]="critical_view360"
    ["Duds/OI-Piranha"]="oi_piranha"
    ["Duds/Circa-3D-Printer"]="circa_3d_printer"
)

for repo in "${!RENAMES[@]}"; do
    new_name="${RENAMES[$repo]}"
    echo -e "${BLUE}📝 Renaming: $repo → $new_name${NC}"
    
    if gh repo rename "$new_name" --repo "$repo" --yes; then
        echo -e "${GREEN}✅ Successfully renamed${NC}"
    else
        echo -e "${RED}❌ Failed to rename${NC}"
    fi
    echo ""
    sleep 2  # Rate limiting
done

echo "======================================================================="
echo "Step 3: Transferring Repositories to Organizations"
echo "======================================================================="
echo ""

# Transfer to duds-production
echo -e "${BLUE}📦 Transferring to duds-production...${NC}"
gh api -X POST repos/Duds/aegrid/transfer -f new_owner=duds-production && \
    echo -e "${GREEN}✅ aegrid transferred${NC}" || \
    echo -e "${RED}❌ Failed to transfer aegrid${NC}"
echo ""
sleep 2

# Transfer to duds-portfolio
echo -e "${BLUE}📦 Transferring to duds-portfolio...${NC}"

for repo in dale_rogers_portfolio portfolio_v3 portfolio; do
    gh api -X POST "repos/Duds/$repo/transfer" -f new_owner=duds-portfolio && \
        echo -e "${GREEN}✅ $repo transferred${NC}" || \
        echo -e "${RED}❌ Failed to transfer $repo${NC}"
    echo ""
    sleep 2
done

echo "======================================================================="
echo "Step 4: Creating New Repositories in duds-templates"
echo "======================================================================="
echo ""

# Create projects_organization (meta repo for management system)
echo -e "${BLUE}📚 Creating projects_organization (management system)...${NC}"
cd /Users/dalerogers/Projects

if gh repo create duds-templates/projects_organization --public --source=. --push \
  --description "Project organization system: analysis, automation scripts, and documentation for managing all repositories"; then
    echo -e "${GREEN}✅ projects_organization created${NC}"
else
    echo -e "${RED}❌ Failed to create projects_organization${NC}"
fi
echo ""

# Create cursor_rules_library
echo -e "${BLUE}📚 Creating cursor_rules_library...${NC}"
cd /Users/dalerogers/Projects/cursor_rules_library

if gh repo create duds-templates/cursor_rules_library --public --source=. --push \
  --description "Centralized Cursor AI rules and commands library organized by technology stack"; then
    echo -e "${GREEN}✅ cursor_rules_library created${NC}"
else
    echo -e "${RED}❌ Failed to create cursor_rules_library${NC}"
fi
echo ""

# Create project_templates
echo -e "${BLUE}📚 Creating project_templates...${NC}"
cd /Users/dalerogers/Projects/templates

if [ ! -d .git ]; then
    git init
    git add .
    git commit -m "Initial commit: Project templates

- Next.js + TypeScript template
- Astro template
- Python FastAPI template
- PowerPages + .NET + Azure template
- Static HTML template
- Cursor rules and commands for each stack"
fi

if gh repo create duds-templates/project_templates --public --source=. --push \
  --description "Production-ready project templates: Next.js, Astro, Python FastAPI, .NET, HTML"; then
    echo -e "${GREEN}✅ project_templates created${NC}"
else
    echo -e "${RED}❌ Failed to create project_templates${NC}"
fi
echo ""

echo "======================================================================="
echo "✅ SETUP COMPLETE"
echo "======================================================================="
echo ""
echo "Next steps:"
echo "1. Run the update_remotes.sh script to update local git remotes"
echo "2. Run ./update_registry.py to refresh project metadata"
echo "3. Verify with ./sync_projects.sh status"
echo ""

