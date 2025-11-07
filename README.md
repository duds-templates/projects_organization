# Projects Directory

Centralized workspace for all development projects with automated organization, analysis, and management tools.

## 🌟 Quick Links

- **Documentation:** [`docs/`](docs/) - Comprehensive guides and reports
- **Scripts:** [`scripts/`](scripts/) - Automation and management tools  
- **Analysis:** [`analysis/`](analysis/) - Project analysis data
- **Registry:** [`.project-registry.json`](.project-registry.json) - Project metadata

## 📊 Overview

**Total Projects:** 19  
**GitHub Repositories:** 23 across 4 locations  
**Organizations:** 3 (production, portfolio, templates)

## 📁 Project Structure

```
~/Projects/
├── active/
│   ├── production/           # Production-ready (1 project)
│   ├── development/          # Active development
│   └── experimental/         # Experiments (7 projects)
├── portfolio/                # Portfolio projects (3)
├── archived/                 # Archived projects (3)
├── learning/                 # Forks and learning (5)
├── work/                     # 🔒 Confidential client work (NEVER synced)
│   └── clients/              # Client consulting projects
├── cursor_rules_library/     # Cursor AI rules (84 rules, 34 commands)
├── templates/                # Project templates (5 stacks)
├── docs/                     # Documentation
├── analysis/                 # Analysis data
├── scripts/                  # Automation scripts
└── .project-registry.json    # Project metadata
```

## 🔒 Confidential Work

The `work/` folder contains confidential client consulting projects:
- ✅ **NEVER synced to GitHub** (excluded in .gitignore)
- ✅ Contains client-specific documentation, analysis, and deliverables
- ✅ Supports .md, .docx, .xlsx, .ipynb files
- ⚠️ **Ensure separate backups** (not version controlled)

**Current Clients:**
- **DCCEEW** (Department of Climate Change, Energy, the Environment and Water)
  - 2025: Technology Framework Pilot
  - 2025: AI Capability Design & Enablement

## 🚀 Quick Start

### View Projects
```bash
# List all projects
cat .project-registry.json | jq '.projects[] | {name, maturity: .maturity.level, tech: .tech_stack.primary_language}'

# By technology
cat .project-registry.json | jq '.projects[] | select(.tech_stack.primary_language == "TypeScript")'
```

### Sync Projects
```bash
scripts/sync_projects.sh status    # Check sync status
scripts/sync_projects.sh pull      # Pull all projects
scripts/sync_projects.sh push      # Push all projects
```

### Health Check
```bash
scripts/check_project_health.sh               # All projects
scripts/check_project_health.sh aegrid        # Specific project
```

### Update Metadata
```bash
scripts/update_registry.py                    # Refresh all metadata
```

## 🏢 GitHub Organizations

### duds-production
Enterprise-grade production systems  
→ https://github.com/duds-production

**Repositories:**
- **aegrid** - Energy grid management platform (9.5/10 maturity)

### duds-portfolio
Portfolio and personal branding projects  
→ https://github.com/duds-portfolio

**Repositories:**
- **dale_rogers_portfolio** - Primary portfolio (Astro) (7.5/10)
- **portfolio_v3** - HTML/CSS portfolio (6.5/10)
- **portfolio** - MDX portfolio

### duds-templates
Reusable templates and development resources  
→ https://github.com/duds-templates

**Repositories:**
- **projects_organization** - This management system
- **cursor_rules_library** - Cursor AI rules and commands
- **project_templates** - 5 stack templates

## 🛠️ Management Tools

| Script | Purpose |
|--------|---------|
| `scripts/sync_projects.sh` | Sync all projects with GitHub |
| `scripts/check_project_health.sh` | Run health checks |
| `scripts/update_registry.py` | Refresh project metadata |
| `scripts/verify_github_setup.sh` | Verify GitHub organization setup |

## 📚 Documentation

- **[Main Guide](docs/README.md)** - Complete overview
- **[Tech Stacks](docs/TECH_STACKS.md)** - Technology breakdown
- **[Maturity Report](docs/MATURITY_REPORT.md)** - Project assessments
- **[Implementation Summary](docs/IMPLEMENTATION_SUMMARY.md)** - Setup history
- **[GitHub Reorganization](docs/GITHUB_REORGANIZATION_SUCCESS.md)** - Organization details

## 🎯 Key Features

- ✅ **Automated Analysis** - Technology stack detection, maturity ranking
- ✅ **Health Monitoring** - Automated health checks across all projects
- ✅ **Sync Management** - One-command sync for all repositories
- ✅ **Organization System** - Structured folders by purpose and maturity
- ✅ **Template Library** - 5 production-ready project templates
- ✅ **Cursor Rules** - 84 rules + 34 commands organized by tech stack
- ✅ **Metadata Registry** - Centralized project information

## 🔄 Regular Maintenance

**Daily:** Check sync status before/after work  
**Weekly:** Run health checks, update registry  
**Monthly:** Review maturity scores, archive candidates

## 📝 Naming Conventions

- **All projects:** snake_case
- **GitHub repos:** snake_case
- **Organizations:** kebab-case (duds-production, duds-portfolio, duds-templates)

## 🌏 Regional Standards

- Australian English spelling
- DD/MM/YYYY date format
- 24-hour time format
- $AUD currency
- Metric measurements

---

**Last Updated:** 07/11/2025  
**System Version:** 1.0.0  
**Managed By:** Automated project organization system

