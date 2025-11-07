#!/bin/bash
# check_project_health.sh - Run health checks on all projects
# Usage: ./check_project_health.sh [project_name]

set -e

PROJECTS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REGISTRY_FILE="$PROJECTS_DIR/.project-registry.json"

# Colours
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

TARGET_PROJECT="${1:-}"

echo "======================================================================="
echo "PROJECT HEALTH CHECK"
echo "======================================================================="
echo ""

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo -e "${RED}Error: jq is not installed. Install with: brew install jq${NC}"
    exit 1
fi

run_health_check() {
    local project_path=$1
    local project_name=$(basename "$project_path")
    
    echo -e "${BLUE}📊 Checking: $project_name${NC}"
    
    if [ ! -d "$project_path" ]; then
        echo -e "${RED}   ❌ Directory not found${NC}"
        echo ""
        return 1
    fi
    
    local issues=0
    local warnings=0
    
    # Check 1: Git repository
    if [ ! -d "$project_path/.git" ]; then
        echo -e "${RED}   ❌ Not a git repository${NC}"
        ((issues++))
    else
        echo -e "${GREEN}   ✓ Git repository${NC}"
    fi
    
    # Check 2: README exists
    if [ -f "$project_path/README.md" ]; then
        local readme_size=$(wc -c < "$project_path/README.md")
        if [ $readme_size -gt 500 ]; then
            echo -e "${GREEN}   ✓ README.md exists (${readme_size} bytes)${NC}"
        else
            echo -e "${YELLOW}   ⚠️  README.md is small (${readme_size} bytes)${NC}"
            ((warnings++))
        fi
    else
        echo -e "${RED}   ❌ No README.md${NC}"
        ((issues++))
    fi
    
    # Check 3: .gitignore exists
    if [ -f "$project_path/.gitignore" ]; then
        echo -e "${GREEN}   ✓ .gitignore exists${NC}"
    else
        echo -e "${YELLOW}   ⚠️  No .gitignore${NC}"
        ((warnings++))
    fi
    
    # Check 4: Uncommitted changes
    if [ -d "$project_path/.git" ]; then
        cd "$project_path"
        if [[ -n $(git status -s) ]]; then
            local change_count=$(git status -s | wc -l)
            echo -e "${YELLOW}   ⚠️  ${change_count} uncommitted changes${NC}"
            ((warnings++))
        else
            echo -e "${GREEN}   ✓ Clean working directory${NC}"
        fi
        cd "$PROJECTS_DIR"
    fi
    
    # Check 5: Package manager files
    local has_package_manager=0
    if [ -f "$project_path/package.json" ]; then
        echo -e "${GREEN}   ✓ package.json exists${NC}"
        has_package_manager=1
        
        # Check for lock file
        if [ -f "$project_path/package-lock.json" ] || [ -f "$project_path/yarn.lock" ] || [ -f "$project_path/pnpm-lock.yaml" ]; then
            echo -e "${GREEN}   ✓ Lock file exists${NC}"
        else
            echo -e "${YELLOW}   ⚠️  No lock file${NC}"
            ((warnings++))
        fi
        
        # Check for node_modules
        if [ ! -d "$project_path/node_modules" ]; then
            echo -e "${YELLOW}   ⚠️  node_modules not found (run npm install)${NC}"
            ((warnings++))
        fi
    fi
    
    if [ -f "$project_path/requirements.txt" ] || [ -f "$project_path/pyproject.toml" ]; then
        echo -e "${GREEN}   ✓ Python dependencies defined${NC}"
        has_package_manager=1
    fi
    
    if [ -f "$project_path/Cargo.toml" ]; then
        echo -e "${GREEN}   ✓ Cargo.toml exists${NC}"
        has_package_manager=1
    fi
    
    # Check 6: Test directory or files
    if [ -d "$project_path/tests" ] || [ -d "$project_path/__tests__" ] || [ -d "$project_path/test" ]; then
        echo -e "${GREEN}   ✓ Test directory exists${NC}"
    elif find "$project_path" -maxdepth 2 -name "*.test.*" -o -name "*.spec.*" | grep -q .; then
        echo -e "${GREEN}   ✓ Test files found${NC}"
    else
        echo -e "${YELLOW}   ⚠️  No tests found${NC}"
        ((warnings++))
    fi
    
    # Summary
    echo ""
    if [ $issues -eq 0 ] && [ $warnings -eq 0 ]; then
        echo -e "${GREEN}   ✅ All checks passed!${NC}"
    elif [ $issues -eq 0 ]; then
        echo -e "${YELLOW}   ⚠️  ${warnings} warnings${NC}"
    else
        echo -e "${RED}   ❌ ${issues} issues, ${warnings} warnings${NC}"
    fi
    
    echo ""
    return $issues
}

# Main execution
if [ -n "$TARGET_PROJECT" ]; then
    # Check specific project
    PROJECT_PATH=$(jq -r ".projects[] | select(.name == \"$TARGET_PROJECT\") | .path" "$REGISTRY_FILE")
    
    if [ -z "$PROJECT_PATH" ] || [ "$PROJECT_PATH" == "null" ]; then
        echo -e "${RED}Error: Project '$TARGET_PROJECT' not found in registry${NC}"
        exit 1
    fi
    
    run_health_check "$PROJECT_PATH"
else
    # Check all projects
    PROJECT_PATHS=$(jq -r '.projects[] | .path' "$REGISTRY_FILE")
    
    TOTAL=0
    PASSED=0
    FAILED=0
    
    while IFS= read -r project_path; do
        ((TOTAL++))
        if run_health_check "$project_path"; then
            ((PASSED++))
        else
            ((FAILED++))
        fi
    done <<< "$PROJECT_PATHS"
    
    echo "======================================================================="
    echo "HEALTH CHECK SUMMARY"
    echo "======================================================================="
    echo "Total projects checked: $TOTAL"
    echo -e "${GREEN}✅ Passed: $PASSED${NC}"
    if [ $FAILED -gt 0 ]; then
        echo -e "${RED}❌ Issues found: $FAILED${NC}"
    fi
    echo "======================================================================="
fi

