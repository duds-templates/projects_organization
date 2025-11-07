#!/bin/bash
# Update local git remotes after repository renaming and organization transfers

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo "======================================================================="
echo "UPDATING LOCAL GIT REMOTES"
echo "======================================================================="
echo ""

# Function to update remote
update_remote() {
    local project_path=$1
    local new_remote=$2
    local project_name=$(basename "$project_path")
    
    if [ ! -d "$project_path" ]; then
        echo -e "${YELLOW}⏭️  Skipped: $project_name (directory not found)${NC}"
        return
    fi
    
    if [ ! -d "$project_path/.git" ]; then
        echo -e "${YELLOW}⏭️  Skipped: $project_name (not a git repo)${NC}"
        return
    fi
    
    cd "$project_path"
    
    local current_remote=$(git config --get remote.origin.url || echo "none")
    
    echo -e "${BLUE}📝 Updating: $project_name${NC}"
    echo "   Current: $current_remote"
    echo "   New: $new_remote"
    
    if git remote set-url origin "$new_remote"; then
        echo -e "${GREEN}✅ Successfully updated${NC}"
    else
        echo -e "${RED}❌ Failed to update${NC}"
    fi
    echo ""
}

# Production
echo "🏭 Production Projects"
update_remote "/Users/dalerogers/Projects/active/production/aegrid" \
    "git@github.com:duds-production/aegrid.git"

# Portfolio
echo "💼 Portfolio Projects"
update_remote "/Users/dalerogers/Projects/portfolio/dale_rogers_portfolio" \
    "git@github.com:duds-portfolio/dale_rogers_portfolio.git"

update_remote "/Users/dalerogers/Projects/portfolio/portfolio_v3" \
    "git@github.com:duds-portfolio/portfolio_v3.git"

update_remote "/Users/dalerogers/Projects/portfolio/portfolio" \
    "git@github.com:duds-portfolio/portfolio.git"

# Experimental (Personal Account - Renamed)
echo "🧪 Experimental Projects (Personal Account)"
update_remote "/Users/dalerogers/Projects/active/experimental/procedural_design_scratch" \
    "git@github.com:Duds/procedural_design_scratch.git"

update_remote "/Users/dalerogers/Projects/active/experimental/bid_writer" \
    "git@github.com:Duds/bid_writer.git"

update_remote "/Users/dalerogers/Projects/active/experimental/bid_writer_mvp" \
    "git@github.com:Duds/bid_writer_mvp.git"

update_remote "/Users/dalerogers/Projects/active/experimental/my_nab" \
    "git@github.com:Duds/my_nab.git"

update_remote "/Users/dalerogers/Projects/active/experimental/google_docs_scripts" \
    "git@github.com:Duds/google_docs_scripts.git"

update_remote "/Users/dalerogers/Projects/active/experimental/capopt_platform" \
    "git@github.com:Duds/capopt_platform.git"

update_remote "/Users/dalerogers/Projects/active/experimental/mowing" \
    "git@github.com:Duds/mowing.git"

# Archived
echo "📦 Archived Projects"
update_remote "/Users/dalerogers/Projects/archived/critical_view360" \
    "git@github.com:Duds/critical_view360.git"

update_remote "/Users/dalerogers/Projects/archived/oi__piranha" \
    "git@github.com:Duds/oi_piranha.git"

# Templates
echo "📚 Template Projects"
update_remote "/Users/dalerogers/Projects/cursor_rules_library" \
    "git@github.com:duds-templates/cursor_rules_library.git"

update_remote "/Users/dalerogers/Projects/templates" \
    "git@github.com:duds-templates/project_templates.git"

echo "======================================================================="
echo "✅ REMOTES UPDATE COMPLETE"
echo "======================================================================="
echo ""
echo "Verify with: ./sync_projects.sh status"
echo ""

