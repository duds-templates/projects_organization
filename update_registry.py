#!/usr/bin/env python3
"""
Update project registry with latest metadata
"""
import sys
import subprocess
from pathlib import Path

# Add Projects dir to path so we can import our scripts
sys.path.insert(0, str(Path(__file__).parent))

print("=" * 70)
print("UPDATING PROJECT REGISTRY")
print("=" * 70)

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
print("  • README.md")
print("  • TECH_STACKS.md")
print("  • MATURITY_REPORT.md")
print("  • project_comparison.json")
print("  • consolidation_recommendations.json")
print("  • cursor_files_inventory.json")
print("=" * 70)

