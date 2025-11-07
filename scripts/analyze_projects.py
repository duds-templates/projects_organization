#!/usr/bin/env python3
"""
Comprehensive project analysis script for comparing local and remote repositories,
identifying technology stacks, and ranking maturity
"""
import json
import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import hashlib

# Configuration
PROJECTS_DIR = Path('/Users/dalerogers/Projects')
GITHUB_REPOS_FILE = PROJECTS_DIR / 'github_repos_duds.json'


def load_github_repos() -> List[Dict[str, Any]]:
    """Load GitHub repository metadata"""
    with open(GITHUB_REPOS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_local_projects() -> List[Dict[str, Any]]:
    """Get list of local projects with basic info"""
    projects = []
    exclude_dirs = {'.git', 'node_modules', '__pycache__', '.venv', 'venv', 
                   'dist', 'build', '.next', 'uploads', 'test-results',
                   'storybook-static', 'playwright-report', '.cursor'}
    
    for item in PROJECTS_DIR.iterdir():
        if item.is_dir() and not item.name.startswith('.') and item.name not in exclude_dirs:
            projects.append({
                'name': item.name,
                'path': str(item),
                'exists': True
            })
    
    return projects


def get_git_info(project_path: Path) -> Dict[str, Any]:
    """Get Git information for a project"""
    git_dir = project_path / '.git'
    
    if not git_dir.exists():
        return {
            'is_git_repo': False,
            'last_commit': None,
            'remote_url': None,
            'branch': None,
            'has_uncommitted': False
        }
    
    try:
        # Get last commit date
        result = subprocess.run(
            ['git', '-C', str(project_path), 'log', '-1', '--format=%ci'],
            capture_output=True, text=True, timeout=5
        )
        last_commit = result.stdout.strip() if result.returncode == 0 else None
        
        # Get remote URL
        result = subprocess.run(
            ['git', '-C', str(project_path), 'config', '--get', 'remote.origin.url'],
            capture_output=True, text=True, timeout=5
        )
        remote_url = result.stdout.strip() if result.returncode == 0 else None
        
        # Get current branch
        result = subprocess.run(
            ['git', '-C', str(project_path), 'rev-parse', '--abbrev-ref', 'HEAD'],
            capture_output=True, text=True, timeout=5
        )
        branch = result.stdout.strip() if result.returncode == 0 else None
        
        # Check for uncommitted changes
        result = subprocess.run(
            ['git', '-C', str(project_path), 'status', '--porcelain'],
            capture_output=True, text=True, timeout=5
        )
        has_uncommitted = bool(result.stdout.strip()) if result.returncode == 0 else False
        
        return {
            'is_git_repo': True,
            'last_commit': last_commit,
            'remote_url': remote_url,
            'branch': branch,
            'has_uncommitted': has_uncommitted
        }
    except Exception as e:
        return {
            'is_git_repo': True,
            'error': str(e)
        }


def detect_tech_stack(project_path: Path) -> Dict[str, Any]:
    """Detect technology stack for a project"""
    stack_info = {
        'primary_language': None,
        'framework': None,
        'build_tools': [],
        'package_manager': None,
        'categories': []
    }
    
    # Check for various config files
    files_to_check = {
        'package.json': 'Node.js/JavaScript',
        'requirements.txt': 'Python',
        'pyproject.toml': 'Python',
        'Cargo.toml': 'Rust',
        'go.mod': 'Go',
        'pom.xml': 'Java',
        'build.gradle': 'Java/Kotlin',
        'Gemfile': 'Ruby',
        'composer.json': 'PHP',
        'Dockerfile': 'Docker',
        'docker-compose.yml': 'Docker',
        '.cursorrules': 'Cursor',
    }
    
    found_files = []
    for filename, tech in files_to_check.items():
        if (project_path / filename).exists():
            found_files.append((filename, tech))
    
    # Analyze package.json if it exists
    package_json = project_path / 'package.json'
    if package_json.exists():
        try:
            with open(package_json, 'r', encoding='utf-8') as f:
                pkg_data = json.load(f)
                deps = {**pkg_data.get('dependencies', {}), **pkg_data.get('devDependencies', {})}
                
                # Detect framework
                if 'next' in deps:
                    stack_info['framework'] = 'Next.js'
                    stack_info['categories'].append('Web/Frontend')
                elif 'react' in deps:
                    stack_info['framework'] = 'React'
                    stack_info['categories'].append('Web/Frontend')
                elif 'vue' in deps:
                    stack_info['framework'] = 'Vue'
                    stack_info['categories'].append('Web/Frontend')
                elif 'astro' in deps:
                    stack_info['framework'] = 'Astro'
                    stack_info['categories'].append('Web/Frontend')
                elif 'express' in deps:
                    stack_info['framework'] = 'Express'
                    stack_info['categories'].append('Backend/API')
                
                # Detect build tools
                if 'vite' in deps:
                    stack_info['build_tools'].append('Vite')
                if 'webpack' in deps:
                    stack_info['build_tools'].append('Webpack')
                if 'typescript' in deps:
                    stack_info['primary_language'] = 'TypeScript'
                else:
                    stack_info['primary_language'] = 'JavaScript'
                
                # Package manager
                if (project_path / 'pnpm-lock.yaml').exists():
                    stack_info['package_manager'] = 'pnpm'
                elif (project_path / 'yarn.lock').exists():
                    stack_info['package_manager'] = 'yarn'
                elif (project_path / 'package-lock.json').exists():
                    stack_info['package_manager'] = 'npm'
                    
        except Exception as e:
            pass
    
    # Check for Python
    if (project_path / 'requirements.txt').exists() or (project_path / 'pyproject.toml').exists():
        stack_info['primary_language'] = 'Python'
        # Check for common frameworks
        if (project_path / 'manage.py').exists():
            stack_info['framework'] = 'Django'
            stack_info['categories'].append('Backend/API')
        elif any((project_path / f).exists() for f in ['app.py', 'main.py']):
            # Could be Flask, FastAPI, etc.
            stack_info['categories'].append('Backend/API')
    
    # Check for Jupyter notebooks
    if list(project_path.glob('*.ipynb')):
        stack_info['categories'].append('Data Science')
    
    # Default to experimental if no clear category
    if not stack_info['categories']:
        stack_info['categories'].append('Experiments')
    
    stack_info['found_files'] = [f[0] for f in found_files]
    
    return stack_info


def assess_maturity(project_path: Path, git_info: Dict, tech_stack: Dict, github_repo: Optional[Dict] = None) -> Dict[str, Any]:
    """Assess project maturity based on various criteria"""
    
    score = 0
    max_score = 10
    details = []
    
    # Documentation (0-2 points)
    readme = project_path / 'README.md'
    if readme.exists():
        readme_size = readme.stat().st_size
        if readme_size > 2000:  # Substantial README
            score += 2
            details.append("Has comprehensive README (2 pts)")
        elif readme_size > 500:
            score += 1
            details.append("Has basic README (1 pt)")
    
    # Check for additional docs
    docs_dir = project_path / 'docs'
    if docs_dir.exists() and list(docs_dir.glob('*.md')):
        score += 0.5
        details.append("Has additional documentation (0.5 pts)")
    
    # Testing (0-2 points)
    test_indicators = [
        'jest.config.js', 'jest.config.ts', 'vitest.config.ts',
        'pytest.ini', 'tests/', '__tests__/', 'test/',
        'playwright.config.ts', '.spec.ts', '.test.ts'
    ]
    
    has_tests = False
    for indicator in test_indicators:
        if '*' in indicator or '.' in indicator:
            if list(project_path.glob(f"**/{indicator}")):
                has_tests = True
                break
        else:
            if (project_path / indicator).exists():
                has_tests = True
                break
    
    if has_tests:
        # Check if tests directory has substantial content
        test_files = list(project_path.glob('**/*.test.*')) + list(project_path.glob('**/*.spec.*'))
        if len(test_files) > 10:
            score += 2
            details.append("Has comprehensive test suite (2 pts)")
        elif len(test_files) > 0:
            score += 1
            details.append("Has tests (1 pt)")
    
    # Configuration & Build Setup (0-2 points)
    config_files = [
        'tsconfig.json', 'eslint.config.js', '.eslintrc.js',
        'prettier.config.js', 'tailwind.config.js', 'vite.config.ts',
        'next.config.ts', 'astro.config.mjs', 'Dockerfile'
    ]
    
    config_count = sum(1 for cf in config_files if (project_path / cf).exists())
    if config_count >= 5:
        score += 2
        details.append("Well-configured build setup (2 pts)")
    elif config_count >= 3:
        score += 1
        details.append("Basic build configuration (1 pt)")
    
    # CI/CD (0-1 point)
    ci_files = [
        '.github/workflows', 'azure-pipelines.yml',
        '.gitlab-ci.yml', 'Jenkinsfile'
    ]
    if any((project_path / cf).exists() for cf in ci_files):
        score += 1
        details.append("Has CI/CD setup (1 pt)")
    
    # Recent Activity (0-1 point)
    if git_info.get('last_commit'):
        try:
            last_commit_date = datetime.fromisoformat(git_info['last_commit'].replace(' +', '+'))
            days_since = (datetime.now(last_commit_date.tzinfo) - last_commit_date).days
            
            if days_since < 30:
                score += 1
                details.append("Recently active (< 30 days) (1 pt)")
            elif days_since < 90:
                score += 0.5
                details.append("Moderately active (< 90 days) (0.5 pts)")
        except:
            pass
    
    # Completeness (0-1 point)
    completeness_items = [
        'LICENSE', '.gitignore', '.env.example',
        'CHANGELOG.md', 'CONTRIBUTING.md'
    ]
    completeness_count = sum(1 for item in completeness_items if (project_path / item).exists())
    if completeness_count >= 3:
        score += 1
        details.append("Project completeness indicators (1 pt)")
    elif completeness_count >= 1:
        score += 0.5
        details.append("Some completeness indicators (0.5 pts)")
    
    # Production Readiness (0-1 point)
    prod_indicators = [
        'docker-compose.yml', '.env.production', 
        'infra/', 'k8s/', 'terraform/'
    ]
    if any((project_path / pi).exists() for pi in prod_indicators):
        score += 1
        details.append("Production deployment setup (1 pt)")
    
    # GitHub metrics (bonus if available)
    if github_repo:
        if github_repo['stargazers_count'] > 0:
            score += 0.5
            details.append("Has GitHub stars (0.5 bonus)")
        if github_repo.get('has_issues') and github_repo['open_issues_count'] > 0:
            details.append(f"Active issues: {github_repo['open_issues_count']}")
    
    # Determine maturity level
    normalized_score = (score / max_score) * 10
    
    if normalized_score >= 8:
        maturity_level = "Mature"
    elif normalized_score >= 5:
        maturity_level = "Developing"
    elif normalized_score >= 2:
        maturity_level = "Experimental"
    else:
        maturity_level = "Archived"
    
    return {
        'score': round(normalized_score, 1),
        'level': maturity_level,
        'details': details,
        'raw_score': round(score, 1),
        'max_score': max_score
    }


def compare_local_remote() -> Dict[str, Any]:
    """Compare local projects with remote repositories"""
    
    print("Loading GitHub repositories...")
    github_repos = load_github_repos()
    github_repos_map = {repo['name'].lower(): repo for repo in github_repos}
    
    print("Scanning local projects...")
    local_projects = get_local_projects()
    local_projects_map = {proj['name'].lower(): proj for proj in local_projects}
    
    comparison = {
        'local_only': [],
        'remote_only': [],
        'both': [],
        'analysis': []
    }
    
    # Find projects that exist in both
    for local_name, local_proj in local_projects_map.items():
        project_path = Path(local_proj['path'])
        
        print(f"\nAnalyzing: {local_proj['name']}")
        
        # Get git info
        git_info = get_git_info(project_path)
        
        # Detect tech stack
        tech_stack = detect_tech_stack(project_path)
        
        # Find matching GitHub repo
        github_repo = None
        for gh_name, gh_repo in github_repos_map.items():
            if gh_name == local_name or gh_name.replace('-', '_') == local_name or local_name.replace('-', '_') == gh_name:
                github_repo = gh_repo
                break
        
        # Assess maturity
        maturity = assess_maturity(project_path, git_info, tech_stack, github_repo)
        
        analysis = {
            'name': local_proj['name'],
            'path': local_proj['path'],
            'git_info': git_info,
            'tech_stack': tech_stack,
            'maturity': maturity,
            'github_repo': github_repo,
            'status': 'both' if github_repo else 'local_only'
        }
        
        if github_repo:
            comparison['both'].append(analysis)
        else:
            comparison['local_only'].append(analysis)
        
        comparison['analysis'].append(analysis)
    
    # Find remote-only repos
    for gh_name, gh_repo in github_repos_map.items():
        found_local = False
        for local_name in local_projects_map.keys():
            if gh_name == local_name or gh_name.replace('-', '_') == local_name or local_name.replace('-', '_') == gh_name:
                found_local = True
                break
        
        if not found_local:
            comparison['remote_only'].append({
                'name': gh_repo['name'],
                'github_repo': gh_repo,
                'status': 'remote_only'
            })
    
    return comparison


def generate_reports(comparison: Dict[str, Any]):
    """Generate analysis reports"""
    
    # Save full comparison
    output_file = PROJECTS_DIR / 'project_comparison.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(comparison, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Saved detailed analysis to: {output_file}")
    
    # Generate summary
    print("\n" + "=" * 70)
    print("PROJECT ANALYSIS SUMMARY")
    print("=" * 70)
    
    print(f"\n📊 Overview:")
    print(f"  • Total local projects: {len(comparison['analysis'])}")
    print(f"  • Total GitHub repos: {len(comparison['both']) + len(comparison['remote_only'])}")
    print(f"  • Synced (exist in both): {len(comparison['both'])}")
    print(f"  • Local only: {len(comparison['local_only'])}")
    print(f"  • Remote only (not downloaded): {len(comparison['remote_only'])}")
    
    # Maturity breakdown
    print(f"\n🎯 Maturity Levels:")
    maturity_counts = {'Mature': 0, 'Developing': 0, 'Experimental': 0, 'Archived': 0}
    for proj in comparison['analysis']:
        level = proj['maturity']['level']
        maturity_counts[level] += 1
    
    for level, count in maturity_counts.items():
        if count > 0:
            print(f"  • {level}: {count}")
    
    # Tech stack breakdown
    print(f"\n💻 Technology Stacks:")
    tech_counts = {}
    for proj in comparison['analysis']:
        primary = proj['tech_stack'].get('primary_language') or 'Unknown'
        tech_counts[primary] = tech_counts.get(primary, 0) + 1
    
    for tech, count in sorted(tech_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  • {tech}: {count}")
    
    # Top mature projects
    print(f"\n⭐ Top Projects by Maturity:")
    sorted_projects = sorted(comparison['analysis'], 
                            key=lambda x: x['maturity']['score'], 
                            reverse=True)[:5]
    
    for i, proj in enumerate(sorted_projects, 1):
        maturity = proj['maturity']
        print(f"  {i}. {proj['name']}: {maturity['score']}/10 ({maturity['level']})")
    
    # Projects needing download
    if comparison['remote_only']:
        print(f"\n📥 Projects to Download:")
        for proj in comparison['remote_only']:
            gh_repo = proj['github_repo']
            print(f"  • {proj['name']}: {gh_repo['language'] or 'Unknown'} - {gh_repo['description'] or 'No description'}")
    
    # Local-only projects
    if comparison['local_only']:
        print(f"\n💾 Local-Only Projects (not on GitHub):")
        for proj in comparison['local_only']:
            print(f"  • {proj['name']}: {proj['tech_stack'].get('primary_language', 'Unknown')}")
    
    print("\n" + "=" * 70)


if __name__ == '__main__':
    print("Starting comprehensive project analysis...\n")
    comparison = compare_local_remote()
    generate_reports(comparison)
    print("\n✅ Analysis complete!")

