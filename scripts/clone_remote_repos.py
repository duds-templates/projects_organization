#!/usr/bin/env python3
"""
Clone all remote repositories that don't exist locally
"""
import json
import subprocess
from pathlib import Path

PROJECTS_DIR = Path('/Users/dalerogers/Projects')
COMPARISON_FILE = PROJECTS_DIR / 'project_comparison.json'


def load_comparison():
    with open(COMPARISON_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def clone_repository(repo_data, destination):
    """Clone a repository"""
    clone_url = repo_data['github_repo']['clone_url']
    repo_name = repo_data['name']
    
    print(f"\n📥 Cloning {repo_name}...")
    print(f"   URL: {clone_url}")
    print(f"   Destination: {destination}/{repo_name}")
    
    try:
        # Use subprocess to clone
        result = subprocess.run(
            ['git', 'clone', clone_url, str(destination / repo_name)],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        if result.returncode == 0:
            print(f"   ✅ Successfully cloned {repo_name}")
            return True
        else:
            print(f"   ❌ Failed to clone {repo_name}: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"   ⏱️  Timeout cloning {repo_name}")
        return False
    except Exception as e:
        print(f"   ❌ Error cloning {repo_name}: {e}")
        return False


def categorize_repo(repo_data):
    """Determine which category a repo should go into"""
    gh_repo = repo_data['github_repo']
    
    # Forks go to learning
    if gh_repo.get('fork'):
        return 'learning'
    
    # Check last update
    from datetime import datetime
    try:
        pushed_date = datetime.fromisoformat(gh_repo['pushed_at'].replace('Z', '+00:00'))
        days_since = (datetime.now(pushed_date.tzinfo) - pushed_date).days
        
        # Very old repos go to archived
        if days_since > 730:  # 2+ years
            return 'archived'
    except:
        pass
    
    # Check size - very small might be templates or experiments
    if gh_repo['size'] < 200:
        return 'active/experimental'
    
    # Portfolio projects
    if 'portfolio' in repo_data['name'].lower():
        return 'portfolio'
    
    # Default to experimental
    return 'active/experimental'


def main():
    print("=" * 70)
    print("CLONING REMOTE REPOSITORIES")
    print("=" * 70)
    
    comparison = load_comparison()
    remote_only = comparison['remote_only']
    
    print(f"\n📊 Found {len(remote_only)} repositories to clone\n")
    
    success_count = 0
    failed_count = 0
    
    for repo in remote_only:
        # Determine destination
        category = categorize_repo(repo)
        destination = PROJECTS_DIR / category
        destination.mkdir(parents=True, exist_ok=True)
        
        # Clone
        if clone_repository(repo, destination):
            success_count += 1
        else:
            failed_count += 1
    
    print("\n" + "=" * 70)
    print("CLONING SUMMARY")
    print("=" * 70)
    print(f"✅ Successfully cloned: {success_count}")
    print(f"❌ Failed: {failed_count}")
    print(f"📁 Total processed: {len(remote_only)}")
    print("=" * 70)


if __name__ == '__main__':
    main()

