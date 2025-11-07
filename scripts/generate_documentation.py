#!/usr/bin/env python3
"""
Generate comprehensive documentation and project registry
"""
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

PROJECTS_DIR = Path('/Users/dalerogers/Projects')
DOCS_DIR = PROJECTS_DIR / 'docs'
ANALYSIS_DIR = PROJECTS_DIR / 'analysis'


def load_data_files():
    """Load all analysis data files"""
    data = {}
    
    # Load comparison data
    comparison_file = ANALYSIS_DIR / 'project_comparison.json'
    if comparison_file.exists():
        with open(comparison_file, 'r') as f:
            data['comparison'] = json.load(f)
    
    # Load GitHub repos
    github_file = ANALYSIS_DIR / 'github_repos_duds.json'
    if github_file.exists():
        with open(github_file, 'r') as f:
            data['github_repos'] = json.load(f)
    
    # Load consolidation recommendations
    consolidation_file = ANALYSIS_DIR / 'consolidation_recommendations.json'
    if consolidation_file.exists():
        with open(consolidation_file, 'r') as f:
            data['consolidation'] = json.load(f)
    
    # Load cursor inventory
    cursor_file = ANALYSIS_DIR / 'cursor_files_inventory.json'
    if cursor_file.exists():
        with open(cursor_file, 'r') as f:
            data['cursor'] = json.load(f)
    
    return data


def generate_project_registry(data: Dict) -> Dict[str, Any]:
    """Generate the master project registry"""
    
    registry = {
        'generated_at': datetime.now().isoformat(),
        'version': '1.0.0',
        'projects': []
    }
    
    # Get comparison data
    comparison = data.get('comparison', {})
    analysis = comparison.get('analysis', [])
    
    # Build registry entries
    for proj in analysis:
        # Adjust for renamed projects
        project_name = proj['name']
        if project_name == 'Aegrid':
            project_name = 'aegrid'
        elif project_name == 'Scratch':
            project_name = 'scratch'
        elif project_name.find('-') > -1 or project_name[0].isupper():
            # Convert to snake_case
            import re
            s1 = project_name.replace('-', '_')
            s2 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', s1)
            s3 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s2)
            project_name = s3.lower()
        
        entry = {
            'name': project_name,
            'original_name': proj['name'],
            'path': proj['path'].replace(proj['name'], project_name),
            'tech_stack': {
                'primary_language': proj['tech_stack'].get('primary_language'),
                'framework': proj['tech_stack'].get('framework'),
                'categories': proj['tech_stack'].get('categories', [])
            },
            'maturity': {
                'score': proj['maturity']['score'],
                'level': proj['maturity']['level']
            },
            'git': {
                'has_repo': proj['git_info']['is_git_repo'],
                'remote_url': proj['git_info'].get('remote_url'),
                'last_commit': proj['git_info'].get('last_commit')
            },
            'github': None,
            'status': 'active',
            'last_updated': datetime.now().isoformat()
        }
        
        # Add GitHub info if available
        if proj.get('github_repo'):
            gh = proj['github_repo']
            entry['github'] = {
                'url': gh['html_url'],
                'description': gh.get('description'),
                'stars': gh.get('stargazers_count', 0),
                'language': gh.get('language'),
                'archived': gh.get('archived', False)
            }
        
        registry['projects'].append(entry)
    
    # Add remote-only projects
    remote_only = comparison.get('remote_only', [])
    for proj in remote_only:
        gh = proj['github_repo']
        
        # Determine where it was cloned
        project_name = gh['name']
        if project_name.find('-') > -1 or project_name[0].isupper():
            import re
            s1 = project_name.replace('-', '_')
            s2 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', s1)
            s3 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s2)
            project_name = s3.lower()
        
        # Determine location based on categorization
        if gh.get('fork'):
            location = f"learning/{project_name}"
        elif 'portfolio' in project_name:
            location = f"portfolio/{project_name}"
        else:
            # Check if it was archived
            try:
                pushed_date = datetime.fromisoformat(gh['pushed_at'].replace('Z', '+00:00'))
                days_since = (datetime.now(pushed_date.tzinfo) - pushed_date).days
                if days_since > 730:
                    location = f"archived/{project_name}"
                else:
                    location = f"active/experimental/{project_name}"
            except:
                location = f"active/experimental/{project_name}"
        
        entry = {
            'name': project_name,
            'original_name': gh['name'],
            'path': str(PROJECTS_DIR / location),
            'tech_stack': {
                'primary_language': gh.get('language'),
                'framework': None,
                'categories': []
            },
            'maturity': {
                'score': None,
                'level': 'Unknown'
            },
            'git': {
                'has_repo': True,
                'remote_url': gh['clone_url'],
                'last_commit': gh['pushed_at']
            },
            'github': {
                'url': gh['html_url'],
                'description': gh.get('description'),
                'stars': gh.get('stargazers_count', 0),
                'language': gh.get('language'),
                'archived': gh.get('archived', False)
            },
            'status': 'active',
            'last_updated': datetime.now().isoformat()
        }
        
        registry['projects'].append(entry)
    
    return registry


def generate_readme(data: Dict, registry: Dict):
    """Generate main README.md"""
    
    comparison = data.get('comparison', {})
    
    readme_content = f"""# Projects Directory

**Last Updated:** {datetime.now().strftime('%d/%m/%Y %H:%M')}

## Overview

This directory contains all projects organised using a structured system with automated tooling for project management, analysis, and synchronisation.

## 📊 Statistics

- **Total Projects:** {len(registry['projects'])}
- **Local Projects:** {len(comparison.get('analysis', []))}
- **GitHub Repositories:** {len(comparison.get('both', [])) + len(comparison.get('remote_only', []))}
- **Synced Projects:** {len(comparison.get('both', []))}

### Maturity Distribution

"""
    
    # Add maturity stats
    maturity_counts = {'Mature': 0, 'Developing': 0, 'Experimental': 0, 'Archived': 0, 'Unknown': 0}
    for proj in registry['projects']:
        level = proj['maturity'].get('level', 'Unknown')
        maturity_counts[level] = maturity_counts.get(level, 0) + 1
    
    for level, count in maturity_counts.items():
        if count > 0:
            readme_content += f"- **{level}:** {count} projects\n"
    
    readme_content += """
### Technology Stacks

"""
    
    # Add tech stack stats
    tech_counts = {}
    for proj in registry['projects']:
        lang = proj['tech_stack'].get('primary_language') or 'Unknown'
        tech_counts[lang] = tech_counts.get(lang, 0) + 1
    
    for tech, count in sorted(tech_counts.items(), key=lambda x: x[1], reverse=True):
        readme_content += f"- **{tech}:** {count} projects\n"
    
    readme_content += """

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

"""
    
    # Add top projects
    sorted_projects = sorted(
        [p for p in registry['projects'] if p['maturity']['score'] is not None],
        key=lambda x: x['maturity']['score'],
        reverse=True
    )[:5]
    
    for i, proj in enumerate(sorted_projects, 1):
        score = proj['maturity']['score']
        level = proj['maturity']['level']
        name = proj['name']
        readme_content += f"{i}. **{name}** - {score}/10 ({level})\n"
    
    readme_content += """

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
"""
    
    return readme_content


def generate_tech_stacks_doc(data: Dict, registry: Dict):
    """Generate TECH_STACKS.md"""
    
    content = f"""# Technology Stacks Breakdown

**Last Updated:** {datetime.now().strftime('%d/%m/%Y %H:%M')}

This document provides a comprehensive breakdown of all projects organised by technology stack.

"""
    
    # Group projects by primary language
    by_language = {}
    for proj in registry['projects']:
        lang = proj['tech_stack'].get('primary_language') or 'Unknown'
        if lang not in by_language:
            by_language[lang] = []
        by_language[lang].append(proj)
    
    # Generate sections for each language
    for lang in sorted(by_language.keys()):
        projects = by_language[lang]
        content += f"\n## {lang} ({len(projects)} projects)\n\n"
        
        # Group by framework
        by_framework = {}
        for proj in projects:
            framework = proj['tech_stack'].get('framework') or 'No Framework'
            if framework not in by_framework:
                by_framework[framework] = []
            by_framework[framework].append(proj)
        
        for framework in sorted(by_framework.keys()):
            if framework != 'No Framework':
                content += f"\n### {framework}\n\n"
            
            for proj in by_framework[framework]:
                maturity = proj['maturity']
                content += f"- **{proj['name']}**"
                if maturity['score']:
                    content += f" ({maturity['score']}/10 - {maturity['level']})"
                if proj.get('github') and proj['github'].get('description'):
                    content += f"\n  - {proj['github']['description']}"
                content += f"\n  - Path: `{proj['path']}`\n"
                if proj['tech_stack'].get('categories'):
                    content += f"  - Categories: {', '.join(proj['tech_stack']['categories'])}\n"
                content += "\n"
    
    return content


def generate_maturity_report(data: Dict, registry: Dict):
    """Generate MATURITY_REPORT.md"""
    
    content = f"""# Project Maturity Report

**Last Updated:** {datetime.now().strftime('%d/%m/%Y %H:%M')}

This report provides detailed maturity assessments for all projects.

## Methodology

Projects are scored on a scale of 0-10 based on:

- **Documentation** (0-2 points): README quality, additional docs
- **Testing** (0-2 points): Test suite presence and coverage
- **Configuration** (0-2 points): Build configs, linting, CI/CD
- **Recent Activity** (0-1 point): Last commit date
- **Completeness** (0-1 point): License, .gitignore, etc.
- **Production Readiness** (0-1 point): Deployment configurations

### Maturity Levels

- **Mature (8-10):** Production-ready, well-documented, actively maintained
- **Developing (5-7):** Core functionality present, needs polish
- **Experimental (2-4):** Early stage, incomplete, or unmaintained
- **Archived (0-1):** Deprecated, superseded, or abandoned

"""
    
    # Group projects by maturity level
    by_maturity = {'Mature': [], 'Developing': [], 'Experimental': [], 'Archived': [], 'Unknown': []}
    for proj in registry['projects']:
        level = proj['maturity'].get('level', 'Unknown')
        by_maturity[level].append(proj)
    
    # Generate sections for each maturity level
    for level in ['Mature', 'Developing', 'Experimental', 'Archived']:
        projects = by_maturity[level]
        if not projects:
            continue
        
        content += f"\n## {level} Projects ({len(projects)})\n\n"
        
        # Sort by score
        sorted_projects = sorted(
            [p for p in projects if p['maturity']['score'] is not None],
            key=lambda x: x['maturity']['score'],
            reverse=True
        )
        
        for proj in sorted_projects:
            score = proj['maturity']['score']
            content += f"\n### {proj['name']} - {score}/10\n\n"
            content += f"- **Tech Stack:** {proj['tech_stack'].get('primary_language', 'Unknown')}"
            if proj['tech_stack'].get('framework'):
                content += f" ({proj['tech_stack']['framework']})"
            content += "\n"
            content += f"- **Path:** `{proj['path']}`\n"
            
            if proj.get('github'):
                content += f"- **GitHub:** {proj['github']['url']}\n"
                if proj['github'].get('description'):
                    content += f"- **Description:** {proj['github']['description']}\n"
            
            content += "\n"
    
    return content


def main():
    print("=" * 70)
    print("GENERATING DOCUMENTATION")
    print("=" * 70)
    
    print("\n📖 Loading analysis data...")
    data = load_data_files()
    
    print("📊 Generating project registry...")
    registry = generate_project_registry(data)
    
    # Save registry
    registry_file = PROJECTS_DIR / '.project-registry.json'
    with open(registry_file, 'w', encoding='utf-8') as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved: {registry_file}")
    
    # Generate README (keep in root for GitHub)
    print("📄 Generating README.md...")
    readme_content = generate_readme(data, registry)
    readme_file = PROJECTS_DIR / 'README.md'
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print(f"✅ Saved: {readme_file}")
    
    # Generate TECH_STACKS.md
    print("📄 Generating TECH_STACKS.md...")
    tech_content = generate_tech_stacks_doc(data, registry)
    tech_file = DOCS_DIR / 'TECH_STACKS.md'
    with open(tech_file, 'w', encoding='utf-8') as f:
        f.write(tech_content)
    print(f"✅ Saved: {tech_file}")
    
    # Generate MATURITY_REPORT.md
    print("📄 Generating MATURITY_REPORT.md...")
    maturity_content = generate_maturity_report(data, registry)
    maturity_file = DOCS_DIR / 'MATURITY_REPORT.md'
    with open(maturity_file, 'w', encoding='utf-8') as f:
        f.write(maturity_content)
    print(f"✅ Saved: {maturity_file}")
    
    print("\n" + "=" * 70)
    print("DOCUMENTATION SUMMARY")
    print("=" * 70)
    print(f"\n✅ Generated {len(registry['projects'])} project entries")
    print(f"✅ Created README.md")
    print(f"✅ Created TECH_STACKS.md")
    print(f"✅ Created MATURITY_REPORT.md")
    print(f"✅ Created .project-registry.json")
    print("\n" + "=" * 70)


if __name__ == '__main__':
    main()

