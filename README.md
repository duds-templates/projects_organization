# Projects Directory

**Last Updated:** 07/11/2025 11:34

## Overview

This directory contains all projects organised using a structured system with automated tooling for project management, analysis, and synchronisation.

## 📊 Statistics

- **Total Projects:** 23
- **Local Projects:** 6
- **GitHub Repositories:** 18
- **Synced Projects:** 1

### Maturity Distribution

- **Experimental:** 3 projects
- **Archived:** 3 projects
- **Unknown:** 17 projects

### Technology Stacks

- **Unknown:** 13 projects
- **TypeScript:** 6 projects
- **JavaScript:** 2 projects
- **CSS:** 1 projects
- **Jupyter Notebook:** 1 projects


## 📁 Directory Structure

```
~/Projects/
├── active/              # Active development projects
│   ├── production/      # Deployed or production-ready
│   ├── development/     # In active development
│   └── experimental/    # Early-stage experiments
├── portfolio/           # Portfolio and personal branding projects
├── archived/            # Archived projects (kept for reference)
├── templates/           # Project templates and starters
├── learning/            # Tutorial follow-alongs and learning projects
└── cursor_rules_library/ # Centralised Cursor rules and commands
```

## 🔧 Management Tools

### Available Scripts

- **`sync_projects.sh`** - Sync all projects with GitHub
- **`update_registry.py`** - Refresh project metadata
- **`check_project_health.sh`** - Run health checks on all projects

### Analysis Files

- **`.project-registry.json`** - Machine-readable project metadata
- **`project_comparison.json`** - Local vs remote comparison analysis
- **`consolidation_recommendations.json`** - Consolidation and archive recommendations
- **`cursor_files_inventory.json`** - Cursor rules and commands inventory

## 📋 Quick Reference

### Top Projects by Maturity

1. **cursor_rules_library** - 2.0/10 (Experimental)
2. **portfolio** - 2.0/10 (Experimental)
3. **active** - 2.0/10 (Experimental)
4. **learning** - 0.0/10 (Archived)
5. **templates** - 0.0/10 (Archived)


## 🚀 Getting Started

### View All Projects

```bash
cat .project-registry.json | jq '.projects[] | {name, maturity: .maturity.level, tech: .tech_stack.primary_language}'
```

### Find Projects by Technology

```bash
# TypeScript projects
cat .project-registry.json | jq '.projects[] | select(.tech_stack.primary_language == "TypeScript") | .name'

# Python projects
cat .project-registry.json | jq '.projects[] | select(.tech_stack.primary_language == "Python") | .name'
```

### Check Project Status

```bash
./check_project_health.sh
```

## 📚 Cursor Rules Library

A centralised repository of Cursor rules and commands organised by technology stack and purpose. See `cursor_rules_library/README.md` for details.

## 🔄 Sync Guidelines

1. **Before starting work:** Run `./sync_projects.sh pull` to get latest changes
2. **After finishing work:** Run `./sync_projects.sh push` to push changes
3. **Weekly:** Run `./update_registry.py` to refresh project metadata

## 📝 Naming Conventions

- All project folders use `snake_case` naming
- No special characters except underscores
- Lowercase only

## 🗃️ Archive Policy

Projects are candidates for archiving if:
- No commits in 2+ years
- Maturity score below 2/10
- Superseded by newer versions
- Forked repositories with no modifications

See `consolidation_recommendations.json` for current recommendations.

---

*Generated automatically by project organisation system*
