# GitHub Organization & Repository Renaming Plan

**Date:** 07/11/2025  
**Approach:** Option A - Organizations + snake_case naming

## Organizations to Create

### 1. duds-production
**Purpose:** Production-ready, actively maintained projects

**Repositories:**
- `aegrid` (from Duds/Aegrid)

### 2. duds-portfolio
**Purpose:** Portfolio and personal branding projects

**Repositories:**
- `dale_rogers_portfolio` (from Duds/dale-rogers-portfolio)
- `portfolio_v3` (from Duds/portfolio-v3)
- `portfolio` (from Duds/portfolio)

### 3. duds-templates
**Purpose:** Project templates and shared resources

**Repositories:**
- `cursor_rules_library` (NEW - to be created)
- `project_templates` (NEW - to be created)

### 4. Personal Account (Duds/)
**Keep for:** Experimental projects, learning repos, forks

**Repositories:**
- `procedural_design_scratch` (from Duds/procedural-design-scratch)
- `capopt_platform` (from Duds/capopt_platform) 
- `bid_writer` (from Duds/BidWriter)
- `bid_writer_mvp` (from Duds/BidWriter_MVP)
- `mowing` (from Duds/mowing)
- `my_nab` (from Duds/MyNAB)
- `google_docs_scripts` (from Duds/GoogleDocsScripts)
- Forks: beanheads, blender_mcp, blinko, llama_index_javascript

## Repository Renaming Map

| Current GitHub Name | New Name | Organization | Action |
|---------------------|----------|--------------|--------|
| Duds/Aegrid | aegrid | duds-production | Rename + Transfer |
| Duds/dale-rogers-portfolio | dale_rogers_portfolio | duds-portfolio | Rename + Transfer |
| Duds/portfolio-v3 | portfolio_v3 | duds-portfolio | Rename + Transfer |
| Duds/portfolio | portfolio | duds-portfolio | Transfer only |
| Duds/procedural-design-scratch | procedural_design_scratch | Duds/ | Rename only |
| Duds/BidWriter | bid_writer | Duds/ | Rename only |
| Duds/BidWriter_MVP | bid_writer_mvp | Duds/ | Rename only |
| Duds/capopt_platform | capopt_platform | Duds/ | Keep as-is |
| Duds/mowing | mowing | Duds/ | Keep as-is |
| Duds/MyNAB | my_nab | Duds/ | Rename only |
| Duds/GoogleDocsScripts | google_docs_scripts | Duds/ | Rename only |
| N/A | cursor_rules_library | duds-templates | Create new |
| N/A | project_templates | duds-templates | Create new |

## Archived Repositories (No Action)

These stay in personal account, will be archived:
- Duds/Circa-3D-Printer → Archive as-is
- Duds/CriticalView360 → Rename to critical_view360, then archive
- Duds/OI-Piranha → Rename to oi_piranha, then archive

## Implementation Steps

### Step 1: Authenticate GitHub CLI

```bash
gh auth login
```

### Step 2: Create Organizations

```bash
# Create organizations via web interface (free tier)
# Go to: https://github.com/organizations/plan
# Create:
# 1. duds-production
# 2. duds-portfolio  
# 3. duds-templates
```

**Manual Steps Required:**
- Organization creation requires web interface
- Choose "Free" plan for open source
- Set organization email
- Skip team member invitations

### Step 3: Rename Repositories

**Pattern:**
```bash
gh repo rename OLD_NAME NEW_NAME --repo OWNER/OLD_NAME
```

**Commands:**
```bash
# Production
gh repo rename Aegrid aegrid --repo Duds/Aegrid

# Portfolio
gh repo rename dale-rogers-portfolio dale_rogers_portfolio --repo Duds/dale-rogers-portfolio
gh repo rename portfolio-v3 portfolio_v3 --repo Duds/portfolio-v3

# Experimental (personal account)
gh repo rename procedural-design-scratch procedural_design_scratch --repo Duds/procedural-design-scratch
gh repo rename BidWriter bid_writer --repo Duds/BidWriter
gh repo rename BidWriter_MVP bid_writer_mvp --repo Duds/BidWriter_MVP
gh repo rename MyNAB my_nab --repo Duds/MyNAB
gh repo rename GoogleDocsScripts google_docs_scripts --repo Duds/GoogleDocsScripts

# Archived (rename before archiving)
gh repo rename CriticalView360 critical_view360 --repo Duds/CriticalView360
gh repo rename OI-Piranha oi_piranha --repo Duds/OI-Piranha
gh repo rename Circa-3D-Printer circa_3d_printer --repo Duds/Circa-3D-Printer
```

### Step 4: Transfer to Organizations

```bash
# To duds-production
gh repo edit aegrid --enable-issues=true --enable-wiki=false
gh api -X POST repos/Duds/aegrid/transfer -f new_owner=duds-production

# To duds-portfolio
gh api -X POST repos/Duds/dale_rogers_portfolio/transfer -f new_owner=duds-portfolio
gh api -X POST repos/Duds/portfolio_v3/transfer -f new_owner=duds-portfolio
gh api -X POST repos/Duds/portfolio/transfer -f new_owner=duds-portfolio

# Note: Transfers require organization to exist first
```

### Step 5: Create New Repositories in duds-templates

```bash
# cursor_rules_library
cd ~/Projects/cursor_rules_library
gh repo create duds-templates/cursor_rules_library --public --source=. --push \
  --description "Centralized Cursor AI rules and commands library organized by technology stack"

# project_templates (if not already initialized)
cd ~/Projects/templates
git init
git add .
git commit -m "Initial commit: Project templates for multiple stacks"
gh repo create duds-templates/project_templates --public --source=. --push \
  --description "Production-ready project templates: Next.js, Astro, Python FastAPI, .NET, HTML"
```

### Step 6: Update Local Git Remotes

After renaming/transferring, update local remotes:

```bash
# Production
cd ~/Projects/active/production/aegrid
git remote set-url origin git@github.com:duds-production/aegrid.git

# Portfolio
cd ~/Projects/portfolio/dale_rogers_portfolio
git remote set-url origin git@github.com:duds-portfolio/dale_rogers_portfolio.git

cd ~/Projects/portfolio/portfolio_v3
git remote set-url origin git@github.com:duds-portfolio/portfolio_v3.git

cd ~/Projects/portfolio/portfolio
git remote set-url origin git@github.com:duds-portfolio/portfolio.git

# Experimental (personal, just renamed)
cd ~/Projects/active/experimental/procedural_design_scratch
git remote set-url origin git@github.com:Duds/procedural_design_scratch.git

cd ~/Projects/active/experimental/bid_writer
git remote set-url origin git@github.com:Duds/bid_writer.git

cd ~/Projects/active/experimental/bid_writer_mvp
git remote set-url origin git@github.com:Duds/bid_writer_mvp.git

cd ~/Projects/active/experimental/my_nab
git remote set-url origin git@github.com:Duds/my_nab.git

cd ~/Projects/active/experimental/google_docs_scripts
git remote set-url origin git@github.com:Duds/google_docs_scripts.git
```

### Step 7: Archive Old Projects

```bash
# Archive after renaming
gh repo archive Duds/critical_view360 --yes
gh repo archive Duds/oi_piranha --yes
gh repo archive Duds/circa_3d_printer --yes
```

### Step 8: Update Repository Settings

For each repository, set:
- Description
- Topics/Tags
- Homepage URL (if applicable)
- Disable unused features (Wiki, Projects, Discussions)

```bash
# Example for aegrid
gh repo edit duds-production/aegrid \
  --description "Enterprise energy grid management platform with Next.js and Azure" \
  --add-topic typescript,nextjs,react,azure,energy-management \
  --enable-wiki=false \
  --enable-projects=false

# Example for dale_rogers_portfolio
gh repo edit duds-portfolio/dale_rogers_portfolio \
  --description "Professional portfolio website built with Astro" \
  --homepage "https://dalerogers.com.au" \
  --add-topic astro,portfolio,typescript,personal-website
```

## Post-Implementation

### Update Project Registry

```bash
cd ~/Projects
./update_registry.py
```

### Verify All Remotes

```bash
cd ~/Projects
./sync_projects.sh status
```

### Update Documentation

Update any documentation that references old GitHub URLs:
- README files
- Documentation
- CI/CD configurations
- External references

## Benefits of This Organization

### Clarity
- Production code clearly separated
- Portfolio projects grouped together
- Templates centralized and reusable

### Professional
- Organizations look more professional
- Better for showcasing to potential employers/clients
- Clear project categorization

### Management
- Easier to set org-level settings
- Can add collaborators per organization
- Better access control

### Discovery
- Topics/tags for filtering
- Organization pages showcase projects
- Consistent naming makes projects easy to find

## Rollback Plan

If issues occur:
- Organizations can be deleted (repos transfer back)
- Repositories can be renamed back
- Remotes can be updated again
- No data loss in any step

## Final Structure

```
Organizations:
├── duds-production/
│   └── aegrid
├── duds-portfolio/
│   ├── dale_rogers_portfolio
│   ├── portfolio_v3
│   └── portfolio
├── duds-templates/
│   ├── cursor_rules_library
│   └── project_templates
└── Duds/ (personal)
    ├── procedural_design_scratch
    ├── capopt_platform
    ├── bid_writer
    ├── bid_writer_mvp
    ├── mowing
    ├── my_nab
    ├── google_docs_scripts
    ├── [forks...]
    └── [archived...]
```

All repositories in snake_case, properly organized, ready for professional presentation! 🚀

