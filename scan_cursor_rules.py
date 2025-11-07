#!/usr/bin/env python3
"""
Scan all projects for Cursor rules and commands
"""
import json
from pathlib import Path
from typing import Dict, List, Any
import hashlib
import shutil

PROJECTS_DIR = Path('/Users/dalerogers/Projects')


def calculate_file_hash(file_path: Path) -> str:
    """Calculate MD5 hash of a file"""
    try:
        with open(file_path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except:
        return None


def scan_project_for_cursor_files(project_path: Path) -> Dict[str, Any]:
    """Scan a single project for Cursor rules and commands"""
    
    cursor_dir = project_path / '.cursor'
    
    result = {
        'project': project_path.name,
        'path': str(project_path),
        'has_cursor_dir': cursor_dir.exists(),
        'rules': [],
        'commands': []
    }
    
    if not cursor_dir.exists():
        return result
    
    # Scan rules directory
    rules_dir = cursor_dir / 'rules'
    if rules_dir.exists():
        for rule_file in rules_dir.rglob('*'):
            if rule_file.is_file():
                result['rules'].append({
                    'filename': rule_file.name,
                    'relative_path': str(rule_file.relative_to(cursor_dir)),
                    'full_path': str(rule_file),
                    'size': rule_file.stat().st_size,
                    'hash': calculate_file_hash(rule_file),
                    'extension': rule_file.suffix
                })
    
    # Scan commands directory
    commands_dir = cursor_dir / 'commands'
    if commands_dir.exists():
        for cmd_file in commands_dir.rglob('*'):
            if cmd_file.is_file():
                result['commands'].append({
                    'filename': cmd_file.name,
                    'relative_path': str(cmd_file.relative_to(cursor_dir)),
                    'full_path': str(cmd_file),
                    'size': cmd_file.stat().st_size,
                    'hash': calculate_file_hash(cmd_file),
                    'extension': cmd_file.suffix
                })
    
    return result


def scan_all_projects() -> List[Dict[str, Any]]:
    """Scan all projects recursively"""
    
    results = []
    exclude_dirs = {'.git', 'node_modules', '__pycache__', '.venv', 'venv', 
                   'dist', 'build', '.next', 'uploads', 'test-results',
                   'storybook-static', 'playwright-report'}
    
    # Scan root level
    for item in PROJECTS_DIR.iterdir():
        if item.is_dir() and not item.name.startswith('.') and item.name not in exclude_dirs:
            result = scan_project_for_cursor_files(item)
            if result['has_cursor_dir']:
                results.append(result)
    
    # Scan organizational subdirectories
    org_dirs = ['active/production', 'active/development', 'active/experimental', 
                'portfolio', 'archived', 'templates', 'learning']
    
    for org_dir in org_dirs:
        org_path = PROJECTS_DIR / org_dir
        if org_path.exists():
            for item in org_path.iterdir():
                if item.is_dir() and not item.name.startswith('.') and item.name not in exclude_dirs:
                    result = scan_project_for_cursor_files(item)
                    if result['has_cursor_dir']:
                        results.append(result)
    
    return results


def identify_duplicates(all_results: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Identify duplicate rules/commands based on hash"""
    
    # Group rules by hash
    rules_by_hash = {}
    commands_by_hash = {}
    
    for project_result in all_results:
        for rule in project_result['rules']:
            if rule['hash']:
                if rule['hash'] not in rules_by_hash:
                    rules_by_hash[rule['hash']] = []
                rules_by_hash[rule['hash']].append({
                    'project': project_result['project'],
                    'file': rule['filename'],
                    'path': rule['full_path']
                })
        
        for command in project_result['commands']:
            if command['hash']:
                if command['hash'] not in commands_by_hash:
                    commands_by_hash[command['hash']] = []
                commands_by_hash[command['hash']].append({
                    'project': project_result['project'],
                    'file': command['filename'],
                    'path': command['full_path']
                })
    
    # Find duplicates
    duplicate_rules = {h: files for h, files in rules_by_hash.items() if len(files) > 1}
    duplicate_commands = {h: files for h, files in commands_by_hash.items() if len(files) > 1}
    
    return {
        'duplicate_rules': duplicate_rules,
        'duplicate_commands': duplicate_commands
    }


def generate_cursor_rules_library_structure():
    """Create the cursor_rules_library directory structure"""
    
    library_path = PROJECTS_DIR / 'cursor_rules_library'
    
    # Create directory structure
    dirs_to_create = [
        'rules/global',
        'rules/tech_stacks/typescript_react',
        'rules/tech_stacks/python',
        'rules/tech_stacks/astro',
        'rules/tech_stacks/general_web',
        'rules/specialised/testing',
        'rules/specialised/documentation',
        'rules/specialised/deployment',
        'rules/project_specific',
        'commands/global',
        'commands/tech_stacks',
        'commands/specialised',
        'scripts'
    ]
    
    for dir_path in dirs_to_create:
        (library_path / dir_path).mkdir(parents=True, exist_ok=True)
    
    return library_path


def main():
    print("=" * 70)
    print("CURSOR RULES & COMMANDS SCAN")
    print("=" * 70)
    
    print("\n🔍 Scanning all projects for .cursor directories...")
    results = scan_all_projects()
    
    # Save results
    output_file = PROJECTS_DIR / 'cursor_files_inventory.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Saved inventory to: {output_file}")
    
    # Analyze results
    total_projects_with_cursor = len(results)
    total_rules = sum(len(r['rules']) for r in results)
    total_commands = sum(len(r['commands']) for r in results)
    
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"\n📊 Projects with .cursor directory: {total_projects_with_cursor}")
    print(f"📄 Total rule files found: {total_rules}")
    print(f"⚡ Total command files found: {total_commands}")
    
    if results:
        print("\n📁 Projects with Cursor files:")
        for result in results:
            rules_count = len(result['rules'])
            commands_count = len(result['commands'])
            print(f"  • {result['project']}: {rules_count} rules, {commands_count} commands")
    
    # Identify duplicates
    print("\n🔍 Analyzing for duplicates...")
    duplicates = identify_duplicates(results)
    
    dup_rules_count = len(duplicates['duplicate_rules'])
    dup_commands_count = len(duplicates['duplicate_commands'])
    
    print(f"\n🔁 Duplicate rules found: {dup_rules_count}")
    print(f"🔁 Duplicate commands found: {dup_commands_count}")
    
    if dup_rules_count > 0:
        print("\n  Duplicate rule files:")
        for hash_val, files in list(duplicates['duplicate_rules'].items())[:5]:
            print(f"\n  • {files[0]['file']} (appears in {len(files)} projects):")
            for f in files:
                print(f"    - {f['project']}")
    
    # Create library structure
    print("\n📚 Creating cursor_rules_library structure...")
    library_path = generate_cursor_rules_library_structure()
    print(f"✅ Created at: {library_path}")
    
    # Save duplicate analysis
    dup_output = PROJECTS_DIR / 'cursor_duplicates_analysis.json'
    with open(dup_output, 'w', encoding='utf-8') as f:
        json.dump(duplicates, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Saved duplicate analysis to: {dup_output}")
    
    print("\n" + "=" * 70)
    print("✅ Cursor scan complete!")
    print("=" * 70)


if __name__ == '__main__':
    main()

