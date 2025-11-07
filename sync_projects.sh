#!/bin/bash
# sync_projects.sh - Sync all projects with GitHub
# Usage: ./sync_projects.sh [pull|push|status]

set -e

PROJECTS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REGISTRY_FILE="$PROJECTS_DIR/.project-registry.json"

# Colours for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No colour

ACTION="${1:-status}"

echo "======================================================================="
echo "PROJECT SYNC TOOL"
echo "======================================================================="
echo ""
echo "Action: $ACTION"
echo ""

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo -e "${RED}Error: jq is not installed. Install with: brew install jq${NC}"
    exit 1
fi

# Get all project paths from registry
PROJECT_PATHS=$(jq -r '.projects[] | select(.git.has_repo == true) | .path' "$REGISTRY_FILE")

COUNT=0
SUCCESS=0
FAILED=0
SKIPPED=0

while IFS= read -r project_path; do
    if [ ! -d "$project_path" ]; then
        echo -e "${YELLOW}⏭️  Skipped: $project_path (directory not found)${NC}"
        ((SKIPPED++))
        continue
    fi
    
    if [ ! -d "$project_path/.git" ]; then
        echo -e "${YELLOW}⏭️  Skipped: $(basename $project_path) (not a git repository)${NC}"
        ((SKIPPED++))
        continue
    fi
    
    ((COUNT++))
    PROJECT_NAME=$(basename "$project_path")
    
    cd "$project_path"
    
    case $ACTION in
        pull)
            echo -e "${BLUE}📥 Pulling: $PROJECT_NAME${NC}"
            if git pull; then
                echo -e "${GREEN}✅ Successfully pulled: $PROJECT_NAME${NC}"
                ((SUCCESS++))
            else
                echo -e "${RED}❌ Failed to pull: $PROJECT_NAME${NC}"
                ((FAILED++))
            fi
            echo ""
            ;;
        
        push)
            echo -e "${BLUE}📤 Pushing: $PROJECT_NAME${NC}"
            
            # Check for uncommitted changes
            if [[ -n $(git status -s) ]]; then
                echo -e "${YELLOW}⚠️  Uncommitted changes found in $PROJECT_NAME${NC}"
                echo -e "${YELLOW}   Please commit changes before pushing${NC}"
                ((SKIPPED++))
            else
                if git push; then
                    echo -e "${GREEN}✅ Successfully pushed: $PROJECT_NAME${NC}"
                    ((SUCCESS++))
                else
                    echo -e "${RED}❌ Failed to push: $PROJECT_NAME${NC}"
                    ((FAILED++))
                fi
            fi
            echo ""
            ;;
        
        status|*)
            echo -e "${BLUE}📊 Status: $PROJECT_NAME${NC}"
            
            # Get current branch
            BRANCH=$(git rev-parse --abbrev-ref HEAD)
            echo "   Branch: $BRANCH"
            
            # Check for uncommitted changes
            if [[ -n $(git status -s) ]]; then
                echo -e "   ${YELLOW}⚠️  Uncommitted changes${NC}"
                git status -s | head -5
            else
                echo -e "   ${GREEN}✓ Clean working directory${NC}"
            fi
            
            # Check if behind/ahead of remote
            git fetch --quiet
            LOCAL=$(git rev-parse @)
            REMOTE=$(git rev-parse @{u} 2>/dev/null || echo "")
            
            if [ -z "$REMOTE" ]; then
                echo -e "   ${YELLOW}⚠️  No remote tracking branch${NC}"
            elif [ "$LOCAL" = "$REMOTE" ]; then
                echo -e "   ${GREEN}✓ Up to date with remote${NC}"
            else
                BASE=$(git merge-base @ @{u})
                if [ "$LOCAL" = "$BASE" ]; then
                    echo -e "   ${YELLOW}⚠️  Behind remote${NC}"
                elif [ "$REMOTE" = "$BASE" ]; then
                    echo -e "   ${YELLOW}⚠️  Ahead of remote${NC}"
                else
                    echo -e "   ${RED}⚠️  Diverged from remote${NC}"
                fi
            fi
            
            ((SUCCESS++))
            echo ""
            ;;
    esac
    
done <<< "$PROJECT_PATHS"

cd "$PROJECTS_DIR"

echo "======================================================================="
echo "SYNC SUMMARY"
echo "======================================================================="
echo "Total projects processed: $COUNT"
echo -e "${GREEN}✅ Success: $SUCCESS${NC}"
if [ $FAILED -gt 0 ]; then
    echo -e "${RED}❌ Failed: $FAILED${NC}"
fi
if [ $SKIPPED -gt 0 ]; then
    echo -e "${YELLOW}⏭️  Skipped: $SKIPPED${NC}"
fi
echo "======================================================================="

