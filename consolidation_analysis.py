#!/usr/bin/env python3
"""
Consolidation Analysis - Identify duplicates, overlapping projects, and archive candidates
"""
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import difflib

PROJECTS_DIR = Path('/Users/dalerogers/Projects')
COMPARISON_FILE = PROJECTS_DIR / 'project_comparison.json'


def load_comparison() -> Dict[str, Any]:
    """Load project comparison data"""
    with open(COMPARISON_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def calculate_name_similarity(name1: str, name2: str) -> float:
    """Calculate similarity between two project names"""
    return difflib.SequenceMatcher(None, name1.lower(), name2.lower()).ratio()


def identify_duplicates_and_overlaps(comparison: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Identify potential duplicate or overlapping projects"""
    
    duplicates = []
    all_projects = comparison['analysis'] + comparison['remote_only']
    
    # Look for similar names
    for i, proj1 in enumerate(all_projects):
        for proj2 in all_projects[i+1:]:
            name1 = proj1['name']
            name2 = proj2['name']
            
            similarity = calculate_name_similarity(name1, name2)
            
            # High similarity threshold
            if similarity > 0.6:
                duplicates.append({
                    'project1': name1,
                    'project2': name2,
                    'similarity': round(similarity * 100, 1),
                    'type': 'name_similarity',
                    'project1_data': proj1,
                    'project2_data': proj2
                })
    
    # Portfolio projects - clear overlap
    portfolio_projects = [p for p in all_projects 
                         if 'portfolio' in p['name'].lower()]
    
    if len(portfolio_projects) > 1:
        duplicates.append({
            'type': 'portfolio_group',
            'projects': [p['name'] for p in portfolio_projects],
            'count': len(portfolio_projects),
            'details': portfolio_projects
        })
    
    # BidWriter variants
    bidwriter_projects = [p for p in all_projects 
                          if 'bidwriter' in p['name'].lower()]
    
    if len(bidwriter_projects) > 1:
        duplicates.append({
            'type': 'bidwriter_group',
            'projects': [p['name'] for p in bidwriter_projects],
            'count': len(bidwriter_projects),
            'details': bidwriter_projects
        })
    
    return duplicates


def identify_archive_candidates(comparison: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Identify projects that should potentially be archived"""
    
    archive_candidates = []
    
    for proj in comparison['analysis']:
        reasons = []
        priority = 0  # 0=low, 1=medium, 2=high
        
        # Criterion 1: Maturity score is very low
        if proj['maturity']['level'] == 'Archived':
            reasons.append("Maturity level is 'Archived' (score: {})".format(proj['maturity']['score']))
            priority = max(priority, 2)
        
        # Criterion 2: No recent activity
        if proj['git_info'].get('last_commit'):
            try:
                last_commit_str = proj['git_info']['last_commit']
                last_commit_date = datetime.fromisoformat(last_commit_str.replace(' +', '+'))
                days_since = (datetime.now(last_commit_date.tzinfo) - last_commit_date).days
                
                if days_since > 730:  # 2+ years
                    reasons.append(f"No commits in {days_since // 365} years")
                    priority = max(priority, 2)
                elif days_since > 365:
                    reasons.append(f"No commits in {days_since} days")
                    priority = max(priority, 1)
            except:
                pass
        elif not proj['git_info']['is_git_repo']:
            reasons.append("Not a git repository")
            priority = max(priority, 1)
        
        # Criterion 3: Fork with no modifications
        if proj.get('github_repo') and proj['github_repo'].get('fork'):
            reasons.append("Fork with no significant modifications")
            priority = max(priority, 1)
        
        # Criterion 4: Very small project size
        if proj.get('github_repo') and proj['github_repo']['size'] < 100:
            reasons.append("Very small repository (< 100 KB)")
            priority = max(priority, 1)
        
        # Criterion 5: No README or documentation
        if not any('README' in detail for detail in proj['maturity']['details']):
            reasons.append("No README or minimal documentation")
            priority = max(priority, 1)
        
        if reasons:
            archive_candidates.append({
                'name': proj['name'],
                'reasons': reasons,
                'priority': priority,
                'maturity': proj['maturity'],
                'project_data': proj
            })
    
    # Check remote repos for archive candidates
    for proj in comparison['remote_only']:
        reasons = []
        priority = 0
        gh_repo = proj['github_repo']
        
        # Fork
        if gh_repo.get('fork'):
            reasons.append("Fork (may not need local copy)")
            priority = max(priority, 1)
        
        # Very old with no recent activity
        try:
            pushed_date = datetime.fromisoformat(gh_repo['pushed_at'].replace('Z', '+00:00'))
            days_since = (datetime.now(pushed_date.tzinfo) - pushed_date).days
            
            if days_since > 730:
                reasons.append(f"No activity in {days_since // 365} years")
                priority = max(priority, 2)
        except:
            pass
        
        # Very small
        if gh_repo['size'] < 100:
            reasons.append("Very small repository")
            priority = max(priority, 1)
        
        if reasons:
            archive_candidates.append({
                'name': proj['name'],
                'reasons': reasons,
                'priority': priority,
                'remote_only': True,
                'project_data': proj
            })
    
    # Sort by priority
    archive_candidates.sort(key=lambda x: (-x['priority'], x['name']))
    
    return archive_candidates


def generate_consolidation_recommendations(duplicates: List[Dict[str, Any]], 
                                          archives: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Generate actionable consolidation recommendations"""
    
    recommendations = []
    
    # Portfolio project recommendations
    portfolio_group = [d for d in duplicates if d.get('type') == 'portfolio_group']
    if portfolio_group:
        group = portfolio_group[0]
        recommendations.append({
            'category': 'consolidation',
            'title': 'Consolidate Portfolio Projects',
            'projects': group['projects'],
            'action': 'combine',
            'recommendation': """
You have 3 portfolio projects:
- dale-rogers-portfolio (Astro, most mature: 7.5/10)
- portfolio-v3 (HTML/CSS/JS, moderate: 6.5/10)
- portfolio (MDX, remote only)

RECOMMENDATION:
1. Keep 'dale-rogers-portfolio' as your main portfolio (it's the most mature)
2. Migrate any unique content from 'portfolio-v3' and 'portfolio' to 'dale-rogers-portfolio'
3. Archive 'portfolio-v3' and 'portfolio' after migration
""",
            'priority': 'HIGH'
        })
    
    # BidWriter recommendations
    bidwriter_group = [d for d in duplicates if d.get('type') == 'bidwriter_group']
    if bidwriter_group:
        group = bidwriter_group[0]
        recommendations.append({
            'category': 'consolidation',
            'title': 'Consolidate BidWriter Projects',
            'projects': group['projects'],
            'action': 'combine',
            'recommendation': """
You have 2 BidWriter projects:
- BidWriter (168 KB, created Oct 2023, TypeScript)
- BidWriter_MVP (427 KB, created Apr 2025, TypeScript)

RECOMMENDATION:
1. Review if BidWriter_MVP supersedes BidWriter
2. If yes, archive BidWriter and rename BidWriter_MVP to just 'bidwriter'
3. If both have unique value, clarify their purposes in READMEs
""",
            'priority': 'MEDIUM'
        })
    
    # Archive recommendations
    high_priority_archives = [a for a in archives if a['priority'] == 2]
    if high_priority_archives:
        recommendations.append({
            'category': 'archive',
            'title': 'High Priority Archive Candidates',
            'projects': [a['name'] for a in high_priority_archives],
            'action': 'archive',
            'recommendation': f"""
{len(high_priority_archives)} projects are strong candidates for archiving:

""" + "\n".join([f"• {a['name']}: {', '.join(a['reasons'])}" 
                 for a in high_priority_archives]),
            'priority': 'HIGH'
        })
    
    # Fork cleanup
    fork_candidates = [a for a in archives if 'Fork' in ' '.join(a['reasons'])]
    if fork_candidates:
        recommendations.append({
            'category': 'cleanup',
            'title': 'Fork Cleanup',
            'projects': [f['name'] for f in fork_candidates],
            'action': 'review',
            'recommendation': f"""
{len(fork_candidates)} forked projects may not need local copies:

""" + "\n".join([f"• {f['name']}" for f in fork_candidates]) + """

RECOMMENDATION:
Review each fork to determine if you've made modifications.
If no modifications, consider removing local copy and just keep GitHub fork.
""",
            'priority': 'LOW'
        })
    
    return recommendations


def generate_report(duplicates: List[Dict[str, Any]], 
                   archives: List[Dict[str, Any]],
                   recommendations: List[Dict[str, Any]]):
    """Generate consolidation report"""
    
    output_file = PROJECTS_DIR / 'consolidation_recommendations.json'
    
    report = {
        'generated_at': datetime.now().isoformat(),
        'duplicates_and_overlaps': duplicates,
        'archive_candidates': archives,
        'recommendations': recommendations
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Saved consolidation analysis to: {output_file}")
    
    # Print summary
    print("\n" + "=" * 70)
    print("CONSOLIDATION & ARCHIVE ANALYSIS")
    print("=" * 70)
    
    print(f"\n🔍 Duplicate/Overlapping Projects Found: {len(duplicates)}")
    for dup in duplicates:
        if dup['type'] == 'portfolio_group':
            print(f"\n  📁 Portfolio Group ({dup['count']} projects):")
            for proj in dup['projects']:
                print(f"     • {proj}")
        elif dup['type'] == 'bidwriter_group':
            print(f"\n  📁 BidWriter Group ({dup['count']} projects):")
            for proj in dup['projects']:
                print(f"     • {proj}")
        elif dup['type'] == 'name_similarity':
            print(f"\n  📁 Similar Names ({dup['similarity']}% match):")
            print(f"     • {dup['project1']}")
            print(f"     • {dup['project2']}")
    
    print(f"\n📦 Archive Candidates Found: {len(archives)}")
    
    # Group by priority
    high_priority = [a for a in archives if a['priority'] == 2]
    medium_priority = [a for a in archives if a['priority'] == 1]
    
    if high_priority:
        print(f"\n  🔴 HIGH PRIORITY ({len(high_priority)}):")
        for arch in high_priority[:5]:  # Show top 5
            print(f"     • {arch['name']}")
            for reason in arch['reasons']:
                print(f"       - {reason}")
    
    if medium_priority:
        print(f"\n  🟡 MEDIUM PRIORITY ({len(medium_priority)}):")
        for arch in medium_priority[:3]:  # Show top 3
            print(f"     • {arch['name']}")
    
    print(f"\n💡 Recommendations Generated: {len(recommendations)}")
    for rec in recommendations:
        priority_emoji = {'HIGH': '🔴', 'MEDIUM': '🟡', 'LOW': '🟢'}
        emoji = priority_emoji.get(rec['priority'], '⚪')
        print(f"\n  {emoji} {rec['priority']}: {rec['title']}")
        print(f"     Action: {rec['action'].upper()}")
        print(f"     Projects: {', '.join(rec['projects'][:3])}{'...' if len(rec['projects']) > 3 else ''}")
    
    print("\n" + "=" * 70)


def main():
    print("Starting consolidation analysis...\n")
    
    comparison = load_comparison()
    
    print("Identifying duplicates and overlapping projects...")
    duplicates = identify_duplicates_and_overlaps(comparison)
    
    print("Identifying archive candidates...")
    archives = identify_archive_candidates(comparison)
    
    print("Generating recommendations...")
    recommendations = generate_consolidation_recommendations(duplicates, archives)
    
    generate_report(duplicates, archives, recommendations)
    
    print("\n✅ Consolidation analysis complete!")


if __name__ == '__main__':
    main()

