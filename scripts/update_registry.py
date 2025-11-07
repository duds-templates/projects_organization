#!/usr/bin/env python3
"""
Update project registry with latest metadata
"""
import sys
import subprocess
from pathlib import Path
import os

# Get the project root directory
PROJECTS_DIR = Path(__file__).parent.parent
SCRIPTS_DIR = PROJECTS_DIR / 'scripts'

print("=" * 70)
print("UPDATING PROJECT REGISTRY")
print("=" * 70)

# Change to scripts directory for execution
os.chdir(SCRIPTS_DIR)

print("\n🔄 Re-running project analysis...")

# Run the analysis script
result = subprocess.run(
    ['python3', 'analyze_projects.py'],
    capture_output=True,
    text=True
)

if result.returncode != 0:
    print(f"\n❌ Analysis failed: {result.stderr}")
    sys.exit(1)

print("\n🔄 Re-running consolidation analysis...")

# Run consolidation analysis
result = subprocess.run(
    ['python3', 'consolidation_analysis.py'],
    capture_output=True,
    text=True
)

if result.returncode != 0:
    print(f"\n❌ Consolidation analysis failed: {result.stderr}")
    sys.exit(1)

print("\n📚 Re-scanning Cursor files...")

# Run cursor scan
result = subprocess.run(
    ['python3', 'scan_cursor_rules.py'],
    capture_output=True,
    text=True
)

if result.returncode != 0:
    print(f"\n❌ Cursor scan failed: {result.stderr}")
    sys.exit(1)

print("\n📄 Regenerating documentation...")

# Regenerate documentation
result = subprocess.run(
    ['python3', 'generate_documentation.py'],
    capture_output=True,
    text=True
)

if result.returncode != 0:
    print(f"\n❌ Documentation generation failed: {result.stderr}")
    sys.exit(1)

print("\n" + "=" * 70)
print("✅ REGISTRY UPDATE COMPLETE")
print("=" * 70)
print("\nUpdated files:")
print("  • .project-registry.json")
print("  • docs/README.md")
print("  • docs/TECH_STACKS.md")
print("  • docs/MATURITY_REPORT.md")
print("  • analysis/project_comparison.json")
print("  • analysis/consolidation_recommendations.json")
print("  • analysis/cursor_files_inventory.json")
print("=" * 70)

