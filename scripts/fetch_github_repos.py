#!/usr/bin/env python3
"""
Fetch all repositories from a GitHub user account
"""
import json
import urllib.request
import urllib.error
from typing import List, Dict, Any

def fetch_user_repos(username: str) -> List[Dict[str, Any]]:
    """
    Fetch all public repositories for a given GitHub username
    """
    repos = []
    page = 1
    per_page = 100
    
    while True:
        url = f"https://api.github.com/users/{username}/repos?per_page={per_page}&page={page}&type=all"
        
        try:
            req = urllib.request.Request(url)
            req.add_header('Accept', 'application/vnd.github.v3+json')
            req.add_header('User-Agent', 'Python-Script')
            
            with urllib.request.urlopen(req, timeout=30) as response:
                page_repos = json.loads(response.read().decode())
                
                if not page_repos:
                    break
                    
                repos.extend(page_repos)
                
                if len(page_repos) < per_page:
                    break
                    
                page += 1
                
        except urllib.error.HTTPError as e:
            print(f"HTTP Error {e.code}: {e.reason}")
            break
        except urllib.error.URLError as e:
            print(f"URL Error: {e.reason}")
            break
        except Exception as e:
            print(f"Error: {e}")
            break
    
    return repos

def extract_repo_metadata(repo: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract relevant metadata from repository object
    """
    return {
        'name': repo['name'],
        'full_name': repo['full_name'],
        'description': repo.get('description', ''),
        'html_url': repo['html_url'],
        'clone_url': repo['clone_url'],
        'ssh_url': repo['ssh_url'],
        'language': repo.get('language', 'Unknown'),
        'size': repo['size'],
        'stargazers_count': repo['stargazers_count'],
        'watchers_count': repo['watchers_count'],
        'forks_count': repo['forks_count'],
        'open_issues_count': repo['open_issues_count'],
        'created_at': repo['created_at'],
        'updated_at': repo['updated_at'],
        'pushed_at': repo['pushed_at'],
        'archived': repo['archived'],
        'disabled': repo['disabled'],
        'fork': repo['fork'],
        'private': repo['private'],
        'default_branch': repo['default_branch'],
        'topics': repo.get('topics', []),
        'visibility': repo.get('visibility', 'public'),
        'has_wiki': repo.get('has_wiki', False),
        'has_pages': repo.get('has_pages', False),
        'has_downloads': repo.get('has_downloads', False),
        'has_issues': repo.get('has_issues', False),
    }

if __name__ == '__main__':
    username = 'Duds'
    print(f"Fetching repositories for user: {username}")
    
    repos = fetch_user_repos(username)
    
    print(f"\nFound {len(repos)} repositories")
    
    # Extract metadata
    repos_metadata = [extract_repo_metadata(repo) for repo in repos]
    
    # Save to JSON
    output_file = '/Users/dalerogers/Projects/github_repos_duds.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(repos_metadata, f, indent=2, ensure_ascii=False)
    
    print(f"\nSaved repository metadata to: {output_file}")
    
    # Print summary
    print("\n=== Summary ===")
    print(f"Total repositories: {len(repos_metadata)}")
    print(f"Archived: {sum(1 for r in repos_metadata if r['archived'])}")
    print(f"Forks: {sum(1 for r in repos_metadata if r['fork'])}")
    print(f"Private: {sum(1 for r in repos_metadata if r['private'])}")
    
    # Language breakdown
    languages = {}
    for repo in repos_metadata:
        lang = repo['language'] or 'Unknown'
        languages[lang] = languages.get(lang, 0) + 1
    
    print("\n=== Languages ===")
    for lang, count in sorted(languages.items(), key=lambda x: x[1], reverse=True):
        print(f"{lang}: {count}")

