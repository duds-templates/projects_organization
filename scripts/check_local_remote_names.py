#!/usr/bin/env python3
"""
Compare local folder names with GitHub repository names
"""
import json
import subprocess
from pathlib import Path

PROJECTS_DIR = Path('/Users/dalerogers/Projects')
GITHUB_REPOS_FILE = PROJECTS_DIR / 'github_repos_duds.json'


def get_git_remote_name(project_path: Path) -> tuple:
    """Get GitHub repo name from remote URL"""
    git_dir = project_path / '.git'
    if not git_dir.exists():
        return None, None
    
    try:
        result = subprocess.run(
            ['git', '-C', str(project_path), 'config', '--get', 'remote.origin.url'],
            capture_output=True, text=True, timeout=5
        )
        
        if result.returncode != 0:
            return None, None
        
        remote_url = result.stdout.strip()
        
        # Extract repo name from URL
        # Examples:
        # https://github.com/Duds/Aegrid.git
        # git@github.com:Duds/Aegrid.git
        
        if 'github.com' in remote_url:
            parts = remote_url.rstrip('.git').split('/')
            repo_name = parts[-1]
            owner = parts[-2].split(':')[-1]
            return owner, repo_name
        elif 'dev.azure.com' in remote_url:
            return 'Azure', 'DevOps'
        
        return None, None
        
    except Exception as e:
        return None, None


def scan_all_projects():
    """Scan all projects and compare names"""
    
    print("=" * 80)
    print("LOCAL vs REMOTE REPOSITORY NAME COMPARISON")
    print("=" * 80)
    print()
    
    # Load GitHub repos for reference
    with open(GITHUB_REPOS_FILE, 'r') as f:
        github_repos = json.load(f)
    
    github_names = {repo['name'].lower(): repo['name'] for repo in github_repos}
    
    comparisons = []
    
    # Scan all project locations
    locations = [
        PROJECTS_DIR,
        PROJECTS_DIR / 'active' / 'production',
        PROJECTS_DIR / 'active' / 'development',
        PROJECTS_DIR / 'active' / 'experimental',
        PROJECTS_DIR / 'portfolio',
        PROJECTS_DIR / 'archived',
        PROJECTS_DIR / 'learning',
    ]
    
    for location in locations:
        if not location.exists():
            continue
        
        for item in location.iterdir():
            if not item.is_dir() or item.name.startswith('.'):
                continue
            
            if item.name in ['cursor_rules_library', 'templates']:
                # Special handling
                owner, remote_name = get_git_remote_name(item)
                comparisons.append({
                    'local_path': str(item.relative_to(PROJECTS_DIR)),
                    'local_name': item.name,
                    'remote_owner': owner or 'NOT CONFIGURED',
                    'remote_name': remote_name or 'NOT CONFIGURED',
                    'match': False,
                    'status': 'NEW - Needs remote'
                })
                continue
            
            owner, remote_name = get_git_remote_name(item)
            
            if not remote_name:
                comparisons.append({
                    'local_path': str(item.relative_to(PROJECTS_DIR)),
                    'local_name': item.name,
                    'remote_owner': 'N/A',
                    'remote_name': 'Not a git repo',
                    'match': False,
                    'status': 'No git repo'
                })
                continue
            
            # Compare names
            local_lower = item.name.lower()
            remote_lower = remote_name.lower()
            
            match = local_lower == remote_lower
            
            # Check for common variations
            local_normalized = local_lower.replace('_', '').replace('-', '')
            remote_normalized = remote_lower.replace('_', '').replace('-', '')
            
            if local_normalized == remote_normalized and not match:
                status = 'MISMATCH - Different case/separators'
            elif match:
                status = 'MATCH ✅'
            else:
                status = 'MISMATCH - Different names'
            
            comparisons.append({
                'local_path': str(item.relative_to(PROJECTS_DIR)),
                'local_name': item.name,
                'remote_owner': owner or 'Unknown',
                'remote_name': remote_name,
                'match': match,
                'status': status
            })
    
    # Print results
    print(f"{'LOCAL FOLDER':<40} {'REMOTE REPO':<30} {'STATUS':<30}")
    print("-" * 100)
    
    matches = 0
    mismatches = 0
    no_remote = 0
    
    for comp in sorted(comparisons, key=lambda x: (x['status'], x['local_path'])):
        local_display = f"{comp['local_path']:<40}"
        remote_display = f"{comp['remote_owner']}/{comp['remote_name']}"[:30]
        status_display = comp['status']
        
        print(f"{local_display} {remote_display:<30} {status_display}")
        
        if comp['match']:
            matches += 1
        elif 'MISMATCH' in comp['status']:
            mismatches += 1
        else:
            no_remote += 1
    
    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"✅ Matches: {matches}")
    print(f"⚠️  Mismatches: {mismatches}")
    print(f"🔴 No remote/Not git: {no_remote}")
    print()
    
    # Specific checks
    print("=" * 80)
    print("SPECIFIC CHECKS")
    print("=" * 80)
    print()
    
    # cursor_rules_library
    cursor_comp = [c for c in comparisons if c['local_name'] == 'cursor_rules_library']
    if cursor_comp:
        print("📚 cursor_rules_library:")
        print(f"   Local: {cursor_comp[0]['local_path']}")
        print(f"   Remote: {cursor_comp[0]['remote_owner']}/{cursor_comp[0]['remote_name']}")
        print(f"   Status: {cursor_comp[0]['status']}")
        if cursor_comp[0]['remote_name'] == 'NOT CONFIGURED':
            print(f"   ⚠️  NOT PUSHED TO GITHUB YET")
    else:
        print("📚 cursor_rules_library: Not found")
    
    print()
    
    # templates
    templates_comp = [c for c in comparisons if c['local_name'] == 'templates']
    if templates_comp:
        print("📦 templates:")
        print(f"   Local: {templates_comp[0]['local_path']}")
        print(f"   Remote: {templates_comp[0]['remote_owner']}/{templates_comp[0]['remote_name']}")
        print(f"   Status: {templates_comp[0]['status']}")
        if templates_comp[0]['remote_name'] == 'NOT CONFIGURED':
            print(f"   ⚠️  NOT PUSHED TO GITHUB YET")
    else:
        print("📦 templates: Not found")
    
    print()
    
    # Projects management system
    print("🏠 Projects Management System (this directory):")
    owner, remote_name = get_git_remote_name(PROJECTS_DIR)
    if remote_name:
        print(f"   Remote: {owner}/{remote_name}")
        print(f"   Status: Configured ✅")
    else:
        print(f"   Status: NOT CONFIGURED ⚠️")
        print(f"   ⚠️  NOT PUSHED TO GITHUB YET")
    
    print()
    print("=" * 80)
    
    return comparisons


if __name__ == '__main__':
    scan_all_projects()

