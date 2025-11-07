# Execute GitHub Reorganization - Step by Step Guide

**Date:** 07/11/2025

Follow these steps in order to complete the GitHub reorganization.

## Prerequisites Checklist

- [ ] GitHub account: Duds
- [ ] GitHub CLI installed ✅
- [ ] SSH keys configured for GitHub

## 🚀 Execution Steps

### Step 1: Authenticate GitHub CLI

```bash
cd ~/Projects
gh auth login
```

**Choose:**
- `GitHub.com`
- `HTTPS` (or SSH if you prefer)
- `Login with a web browser`
- Follow browser prompts
- Grant all requested permissions

**Verify:**
```bash
gh auth status
# Should show: ✓ Logged in to github.com as Duds
```

---

### Step 2: Create GitHub Organizations

**Manual Step - Web Interface Required**

1. Go to https://github.com/organizations/plan
2. Click "Create a free organization"
3. Create these 3 organizations:

   **Organization 1: duds-production**
   - Name: `duds-production`
   - Contact email: Your email
   - Belongs to: My personal account
   - Plan: Free (for open source)
   
   **Organization 2: duds-portfolio**
   - Name: `duds-portfolio`
   - Contact email: Your email
   - Belongs to: My personal account
   - Plan: Free
   
   **Organization 3: duds-templates**
   - Name: `duds-templates`
   - Contact email: Your email
   - Belongs to: My personal account
   - Plan: Free

4. Skip team member invitations (can add later)
5. Skip other setup steps

---

### Step 3: Run Organization Setup Script

This will rename all repositories and transfer them to organizations:

```bash
cd ~/Projects
./github_org_setup.sh
```

**What it does:**
- ✅ Checks authentication
- ✅ Verifies organizations exist
- ✅ Renames 11 repositories to snake_case
- ✅ Transfers repositories to appropriate organizations
- ✅ Creates new repositories (cursor_rules_library, project_templates)

**Expected Output:**
```
✅ Renamed: Aegrid → aegrid
✅ Renamed: dale-rogers-portfolio → dale_rogers_portfolio
✅ Renamed: portfolio-v3 → portfolio_v3
...
✅ Transferred: aegrid → duds-production
✅ Transferred: dale_rogers_portfolio → duds-portfolio
...
```

**Estimated Time:** 5-10 minutes (due to API rate limiting)

---

### Step 4: Update Local Git Remotes

After repositories are renamed and transferred, update local git configurations:

```bash
cd ~/Projects
./update_remotes.sh
```

**What it does:**
- Updates all local repositories to point to new GitHub URLs
- Handles organization transfers
- Handles renamed repositories

---

### Step 5: Archive Old/Inactive Projects

Archive projects that are no longer active:

```bash
# Archive old projects
gh repo archive Duds/critical_view360 --yes
gh repo archive Duds/oi_piranha --yes
gh repo archive Duds/circa_3d_printer --yes
```

**These will:**
- Become read-only on GitHub
- Still be accessible for reference
- Can be unarchived later if needed

---

### Step 6: Update Repository Metadata

Add descriptions and topics to repositories for better discoverability:

```bash
# duds-production/aegrid
gh repo edit duds-production/aegrid \
  --description "Enterprise energy grid management platform with Next.js, TypeScript, and Azure" \
  --add-topic typescript,nextjs,react,azure,energy-management,iso-55000 \
  --enable-wiki=false

# duds-portfolio/dale_rogers_portfolio
gh repo edit duds-portfolio/dale_rogers_portfolio \
  --description "Professional portfolio website built with Astro and TypeScript" \
  --homepage "https://dalerogers.com.au" \
  --add-topic astro,portfolio,typescript,personal-website

# duds-portfolio/portfolio_v3
gh repo edit duds-portfolio/portfolio_v3 \
  --description "Portfolio website v3 - HTML/CSS/JavaScript" \
  --add-topic portfolio,html,css,javascript

# duds-portfolio/portfolio
gh repo edit duds-portfolio/portfolio \
  --description "Portfolio website built with MDX" \
  --add-topic portfolio,mdx

# duds-templates/cursor_rules_library
gh repo edit duds-templates/cursor_rules_library \
  --description "Centralized Cursor AI rules and commands organized by tech stack" \
  --add-topic cursor,ai,development,rules,automation

# duds-templates/project_templates
gh repo edit duds-templates/project_templates \
  --description "Production-ready templates: Next.js, Astro, FastAPI, .NET, HTML" \
  --add-topic templates,scaffolding,nextjs,astro,dotnet,python

# Duds/procedural_design_scratch
gh repo edit Duds/procedural_design_scratch \
  --description "Experimental procedural design and generative art with Python" \
  --add-topic python,jupyter,procedural-generation,design,experimental

# Duds/bid_writer
gh repo edit Duds/bid_writer \
  --description "Bid writing assistance tool" \
  --add-topic typescript,experimental

# Duds/bid_writer_mvp
gh repo edit Duds/bid_writer_mvp \
  --description "Bid writing tool MVP" \
  --add-topic typescript,mvp,experimental

# Duds/my_nab
gh repo edit Duds/my_nab \
  --description "Modern financial management application with Next.js and PostgreSQL" \
  --add-topic typescript,nextjs,prisma,postgresql,finance

# Duds/capopt_platform
gh repo edit Duds/capopt_platform \
  --description "Capital optimization platform" \
  --add-topic typescript,experimental

# Duds/mowing
gh repo edit Duds/mowing \
  --description "Mowing service management application" \
  --add-topic typescript,nextjs

# Duds/google_docs_scripts
gh repo edit Duds/google_docs_scripts \
  --description "Google Apps Scripts for document automation" \
  --add-topic google-apps-script,automation
```

---

### Step 7: Final Verification

```bash
cd ~/Projects

# Check all remotes updated correctly
./sync_projects.sh status

# Update project registry with new URLs
./update_registry.py

# View new organization on GitHub
gh repo list duds-production
gh repo list duds-portfolio
gh repo list duds-templates
gh repo list Duds --limit 20
```

---

## 📊 Expected Final Structure

```
GitHub Organizations:

duds-production/
  └── aegrid (Enterprise production system)

duds-portfolio/
  ├── dale_rogers_portfolio (Primary portfolio)
  ├── portfolio_v3 (Alternative portfolio)
  └── portfolio (MDX portfolio)

duds-templates/
  ├── cursor_rules_library (Cursor AI rules & commands)
  └── project_templates (5 stack templates)

Duds/ (Personal Account)
  ├── procedural_design_scratch (Experimental Python)
  ├── capopt_platform (Experimental)
  ├── bid_writer (Experimental)
  ├── bid_writer_mvp (Experimental)
  ├── mowing (Experimental)
  ├── my_nab (Financial app)
  ├── google_docs_scripts (Utility)
  ├── beanheads (Fork)
  ├── blender_mcp (Fork)
  ├── blinko (Fork)
  ├── llama_index_javascript (Fork)
  ├── critical_view360 (Archived)
  ├── oi_piranha (Archived)
  └── circa_3d_printer (Archived)
```

All repositories in **snake_case**, properly organized! ✨

---

## 🔧 Troubleshooting

### Authentication Issues

If `gh auth status` fails:
```bash
gh auth logout
gh auth login
```

### API Rate Limiting

If you hit rate limits, wait 1-2 minutes between operations.

### Transfer Failures

If transfer fails:
- Ensure organization exists
- Ensure you have admin rights on organization
- Retry the specific transfer command

### Remote Update Failures

If remote update fails:
```bash
cd /path/to/project
git remote -v  # Check current remote
git remote remove origin
git remote add origin git@github.com:new-org/new-name.git
```

---

## 📝 Post-Implementation

After completing all steps:

1. **Update Documentation**
   - Check for hardcoded GitHub URLs in docs
   - Update CI/CD configurations
   - Update external references

2. **Test Repository Access**
   ```bash
   cd ~/Projects/active/production/aegrid
   git fetch
   git pull
   ```

3. **Share New Organization URLs**
   - Production: https://github.com/duds-production
   - Portfolio: https://github.com/duds-portfolio
   - Templates: https://github.com/duds-templates

---

## ⏱️ Estimated Time

- **Manual Steps (Steps 1-2):** 10-15 minutes
- **Automated Steps (Steps 3-6):** 10-15 minutes
- **Total:** ~30 minutes

---

## 🎯 Success Criteria

- [ ] All organizations created
- [ ] All repositories renamed to snake_case
- [ ] Repositories transferred to correct organizations
- [ ] New repositories created (cursor_rules_library, project_templates)
- [ ] Local remotes updated
- [ ] Old projects archived
- [ ] Repository descriptions and topics added
- [ ] All projects sync successfully

---

*Ready to execute when you authenticate GitHub CLI!*

