#!/usr/bin/env python3
"""
Rename all project folders to snake_case
"""
import re
from pathlib import Path
import shutil

PROJECTS_DIR = Path('/Users/dalerogers/Projects')


def to_snake_case(name: str) -> str:
    """Convert a string to snake_case"""
    # Replace hyphens with underscores
    s1 = name.replace('-', '_')
    
    # Insert underscore before uppercase letters (for PascalCase/camelCase)
    s2 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', s1)
    s3 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s2)
    
    # Convert to lowercase
    return s3.lower()


def get_all_projects() -> list:
    """Get all project directories that need renaming"""
    projects = []
    
    # Root level projects
    exclude_dirs = {'active', 'portfolio', 'archived', 'templates', 'learning', 
                   '.git', 'node_modules', '__pycache__', 'cursor_rules_library'}
    
    for item in PROJECTS_DIR.iterdir():
        if item.is_dir() and not item.name.startswith('.') and item.name not in exclude_dirs:
            projects.append(item)
    
    # Projects in organizational folders
    org_dirs = ['active/production', 'active/development', 'active/experimental', 
                'portfolio', 'archived', 'templates', 'learning']
    
    for org_dir in org_dirs:
        org_path = PROJECTS_DIR / org_dir
        if org_path.exists():
            for item in org_path.iterdir():
                if item.is_dir() and not item.name.startswith('.'):
                    projects.append(item)
    
    return projects


def create_rename_plan() -> list:
    """Create a plan for renaming all projects"""
    projects = get_all_projects()
    rename_plan = []
    
    for project_path in projects:
        old_name = project_path.name
        new_name = to_snake_case(old_name)
        
        if old_name != new_name:
            new_path = project_path.parent / new_name
            rename_plan.append({
                'old_path': project_path,
                'old_name': old_name,
                'new_path': new_path,
                'new_name': new_name
            })
    
    return rename_plan


def execute_renames(rename_plan: list, dry_run: bool = False) -> dict:
    """Execute the rename operations"""
    results = {
        'success': [],
        'skipped': [],
        'failed': []
    }
    
    for item in rename_plan:
        old_path = item['old_path']
        new_path = item['new_path']
        
        # Check if target already exists
        if new_path.exists():
            results['skipped'].append({
                **item,
                'reason': 'Target already exists'
            })
            continue
        
        if dry_run:
            results['success'].append(item)
            continue
        
        try:
            # Rename the directory
            old_path.rename(new_path)
            results['success'].append(item)
            print(f"✅ Renamed: {item['old_name']} → {item['new_name']}")
        except Exception as e:
            results['failed'].append({
                **item,
                'error': str(e)
            })
            print(f"❌ Failed: {item['old_name']} - {e}")
    
    return results


def main():
    print("=" * 70)
    print("PROJECT RENAMING TO snake_case")
    print("=" * 70)
    
    print("\n🔍 Analyzing project names...")
    rename_plan = create_rename_plan()
    
    if not rename_plan:
        print("\n✅ All projects already use snake_case naming!")
        return
    
    print(f"\n📋 Found {len(rename_plan)} projects to rename:\n")
    
    for item in rename_plan:
        print(f"  {item['old_name']}")
        print(f"    → {item['new_name']}")
        print(f"    📁 {item['old_path'].parent}")
        print()
    
    # Execute renames
    print("\n🔄 Executing renames...")
    results = execute_renames(rename_plan, dry_run=False)
    
    # Print summary
    print("\n" + "=" * 70)
    print("RENAME SUMMARY")
    print("=" * 70)
    print(f"\n✅ Successfully renamed: {len(results['success'])}")
    print(f"⏭️  Skipped: {len(results['skipped'])}")
    print(f"❌ Failed: {len(results['failed'])}")
    
    if results['skipped']:
        print("\n⏭️  Skipped projects:")
        for item in results['skipped']:
            print(f"  • {item['old_name']}: {item['reason']}")
    
    if results['failed']:
        print("\n❌ Failed projects:")
        for item in results['failed']:
            print(f"  • {item['old_name']}: {item['error']}")
    
    print("\n" + "=" * 70)
    print("✅ Renaming complete!")
    print("=" * 70)


if __name__ == '__main__':
    main()

