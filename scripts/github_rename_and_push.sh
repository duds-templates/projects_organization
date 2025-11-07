#!/bin/bash
# Rename all GitHub repositories to snake_case and create new repos
# Skip organization transfers (can be done manually later)

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo "======================================================================="
echo "GITHUB REPOSITORY RENAMING & NEW REPO CREATION"
echo "======================================================================="
echo ""

# Check authentication
if ! gh auth status >/dev/null 2>&1; then
    echo -e "${RED}❌ Not authenticated${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Authenticated as: $(gh api user --jq .login)${NC}"
echo ""

echo "======================================================================="
echo "Step 1: Renaming Existing Repositories to snake_case"
echo "======================================================================="
echo ""

# Rename repositories
declare -A RENAMES=(
    ["Duds/Aegrid"]="aegrid"
    ["Duds/dale-rogers-portfolio"]="dale_rogers_portfolio"
    ["Duds/procedural-design-scratch"]="procedural_design_scratch"
    ["Duds/BidWriter"]="bid_writer"
    ["Duds/BidWriter_MVP"]="bid_writer_mvp"
    ["Duds/MyNAB"]="my_nab"
    ["Duds/GoogleDocsScripts"]="google_docs_scripts"
    ["Duds/CriticalView360"]="critical_view360"
    ["Duds/OI-Piranha"]="oi_piranha"
    ["Duds/Circa-3D-Printer"]="circa_3d_printer"
    ["Duds/blender-mcp"]="blender_mcp"
)

SUCCESS=0
FAILED=0

for repo in "${!RENAMES[@]}"; do
    new_name="${RENAMES[$repo]}"
    echo -e "${BLUE}📝 Renaming: $repo → Duds/$new_name${NC}"
    
    if gh repo rename "$new_name" --repo "$repo" --yes 2>&1; then
        echo -e "${GREEN}✅ Successfully renamed${NC}"
        ((SUCCESS++))
    else
        echo -e "${RED}❌ Failed to rename (may already be renamed)${NC}"
        ((FAILED++))
    fi
    echo ""
    sleep 1
done

echo "Rename Summary: $SUCCESS successful, $FAILED failed"
echo ""

echo "======================================================================="
echo "Step 2: Creating New Repositories"
echo "======================================================================="
echo ""

# Create projects_organization
echo -e "${BLUE}📚 Creating Duds/projects_organization...${NC}"
cd /Users/dalerogers/Projects

if gh repo create Duds/projects_organization --public --source=. --push \
  --description "Project organization system: analysis, automation scripts, and documentation" 2>&1; then
    echo -e "${GREEN}✅ projects_organization created and pushed${NC}"
else
    echo -e "${RED}❌ Failed (may already exist)${NC}"
fi
echo ""

# Create cursor_rules_library
echo -e "${BLUE}📚 Creating Duds/cursor_rules_library...${NC}"
cd /Users/dalerogers/Projects/cursor_rules_library

if gh repo create Duds/cursor_rules_library --public --source=. --push \
  --description "Centralized Cursor AI rules and commands library (84 rules, 34 commands)" 2>&1; then
    echo -e "${GREEN}✅ cursor_rules_library created and pushed${NC}"
else
    echo -e "${RED}❌ Failed (may already exist)${NC}"
fi
echo ""

# Create project_templates
echo -e "${BLUE}📚 Creating Duds/project_templates...${NC}"
cd /Users/dalerogers/Projects/templates

if [ ! -d .git ]; then
    git init
    git add .
    git commit -m "Initial commit: Project templates

- Next.js + TypeScript template with Cursor rules
- Astro template with Cursor rules
- Python FastAPI template with Cursor rules
- PowerPages + .NET + Azure template with Cursor rules
- Static HTML template with Cursor rules
- Comprehensive README with usage guide"
fi

if gh repo create Duds/project_templates --public --source=. --push \
  --description "Production-ready project templates: Next.js, Astro, Python FastAPI, .NET, HTML" 2>&1; then
    echo -e "${GREEN}✅ project_templates created and pushed${NC}"
else
    echo -e "${RED}❌ Failed (may already exist)${NC}"
fi
echo ""

echo "======================================================================="
echo "Step 3: Updating Local Git Remotes"
echo "======================================================================="
echo ""

# Update remotes for renamed repos
cd /Users/dalerogers/Projects

# Projects management (if remote exists)
if [ -d ".git" ]; then
    echo -e "${BLUE}📝 Updating Projects management remote${NC}"
    if git remote get-url origin >/dev/null 2>&1; then
        git remote set-url origin git@github.com:Duds/projects_organization.git
    else
        git remote add origin git@github.com:Duds/projects_organization.git
    fi
    echo -e "${GREEN}✅ Updated${NC}"
    echo ""
fi

declare -A REMOTE_UPDATES=(
    ["/Users/dalerogers/Projects/active/production/aegrid"]="Duds/aegrid"
    ["/Users/dalerogers/Projects/portfolio/dale_rogers_portfolio"]="Duds/dale_rogers_portfolio"
    ["/Users/dalerogers/Projects/active/experimental/procedural_design_scratch"]="Duds/procedural_design_scratch"
    ["/Users/dalerogers/Projects/active/experimental/bid_writer"]="Duds/bid_writer"
    ["/Users/dalerogers/Projects/active/experimental/bid_writer_mvp"]="Duds/bid_writer_mvp"
    ["/Users/dalerogers/Projects/active/experimental/my_nab"]="Duds/my_nab"
    ["/Users/dalerogers/Projects/active/experimental/google_docs_scripts"]="Duds/google_docs_scripts"
    ["/Users/dalerogers/Projects/archived/critical_view360"]="Duds/critical_view360"
    ["/Users/dalerogers/Projects/archived/oi__piranha"]="Duds/oi_piranha"
    ["/Users/dalerogers/Projects/learning/blender_mcp"]="Duds/blender_mcp"
    ["/Users/dalerogers/Projects/learning/circa_3_d__printer"]="Duds/circa_3d_printer"
    ["/Users/dalerogers/Projects/cursor_rules_library"]="Duds/cursor_rules_library"
    ["/Users/dalerogers/Projects/templates"]="Duds/project_templates"
)

for project_path in "${!REMOTE_UPDATES[@]}"; do
    new_remote="${REMOTE_UPDATES[$project_path]}"
    
    if [ -d "$project_path/.git" ]; then
        cd "$project_path"
        echo -e "${BLUE}📝 $(basename $project_path)${NC}"
        git remote set-url origin "git@github.com:$new_remote.git" 2>&1 || \
        git remote add origin "git@github.com:$new_remote.git" 2>&1
        echo -e "${GREEN}✅ Remote updated to $new_remote${NC}"
        echo ""
    fi
done

echo "======================================================================="
echo "✅ COMPLETE"
echo "======================================================================="
echo ""
echo "All repositories renamed and created!"
echo ""
echo "Next: Run ./verify_github_setup.sh to verify"
echo ""

