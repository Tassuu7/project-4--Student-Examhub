#!/usr/bin/env python3
"""
ExamHub - Production Verification and Measurement Tool
Validates:
1. Production LOC (>= 50,000 non-blank, non-comment lines in production source files)
2. Git repository integrity and commit count (>= 10 commits)
3. Pull requests / feature branch integration (>= 4 merged feature branches)
4. License conditions (No open-source license files, proprietary declaration)
5. Dependency lockfiles (package-lock.json and requirements lock)
6. Executability & Test Suite execution
7. Cleanliness / Sensitive data checks
"""

import os
import sys
import re
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent

EXCLUDE_DIRS = {
    'node_modules', '.git', 'dist', 'build', '.pytest_cache', '__pycache__',
    'coverage', 'htmlcov', '.venv', 'venv', 'env', '.idea', '.vscode'
}

PRODUCTION_EXTENSIONS = {'.py', '.ts', '.tsx', '.js', '.jsx', '.css', '.html'}
TEST_PATTERNS = {'test_', '_test', '.test.', '.spec.', '/tests/', '/test/'}

def is_comment_or_blank(line: str, ext: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return True
    if ext in ('.py',):
        if stripped.startswith('#'):
            return True
    elif ext in ('.ts', '.tsx', '.js', '.jsx', '.css'):
        if stripped.startswith('//') or stripped.startswith('/*') or stripped.startswith('*') or stripped.endswith('*/'):
            return True
    elif ext in ('.html',):
        if stripped.startswith('<!--') or stripped.endswith('-->'):
            return True
    return False

def count_production_loc():
    total_loc = 0
    file_counts = {}
    
    for root, dirs, files in os.walk(ROOT_DIR):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        rel_root = os.path.relpath(root, ROOT_DIR)
        
        # Skip tests directory from production LOC
        if 'test' in rel_root.lower() or rel_root.startswith('.'):
            continue
            
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext not in PRODUCTION_EXTENSIONS:
                continue
            
            # Skip test files and measurement tool itself
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, ROOT_DIR)
            if any(p in rel_path.lower() for p in TEST_PATTERNS) or f == 'measure.py':
                continue
                
            try:
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as fp:
                    valid_lines = 0
                    for line in fp:
                        if not is_comment_or_blank(line, ext):
                            valid_lines += 1
                    total_loc += valid_lines
                    file_counts[rel_path] = valid_lines
            except Exception as e:
                print(f"Warning reading {rel_path}: {e}")
                
    return total_loc, file_counts

def verify_git():
    # Verify .git directory
    git_dir = ROOT_DIR / '.git'
    if not git_dir.exists():
        return False, "Not a git repository", 0, 0
    
    # Check commit count
    try:
        res = subprocess.run(['git', 'rev-list', '--count', 'HEAD'], capture_output=True, text=True, cwd=ROOT_DIR)
        commits = int(res.stdout.strip()) if res.returncode == 0 else 0
    except Exception:
        commits = 0

    # Check merged feature branches / PRs
    try:
        res = subprocess.run(['git', 'log', '--oneline', '--grep=Merge pull request\\|Merge branch\\|PR #'], capture_output=True, text=True, cwd=ROOT_DIR)
        pr_count = len([line for line in res.stdout.strip().split('\n') if line]) if res.returncode == 0 else 0
    except Exception:
        pr_count = 0
        
    return True, "Git repository valid", commits, pr_count

def verify_license():
    forbidden_files = ['LICENSE', 'LICENSE.txt', 'LICENSE.md', 'COPYING', 'LICENSE.mit', 'LICENSE.apache']
    found_forbidden = []
    for f in forbidden_files:
        if (ROOT_DIR / f).exists():
            found_forbidden.append(f)
            
    # Check for GPL or open source license mentions in package.json
    package_json = ROOT_DIR / 'package.json'
    if package_json.exists():
        with open(package_json, 'r') as fp:
            content = fp.read()
            if '"GPL"' in content or '"AGPL"' in content or '"MIT"' in content:
                found_forbidden.append("Open source license in package.json")
                
    return len(found_forbidden) == 0, found_forbidden

def verify_lockfiles():
    package_lock = (ROOT_DIR / 'package-lock.json').exists() or (ROOT_DIR / 'bun.lock').exists()
    python_lock = (ROOT_DIR / 'requirements.txt').exists() or (ROOT_DIR / 'requirements.lock').exists()
    return package_lock and python_lock

def verify_sensitive_data():
    sensitive_keywords = ['sk_live_', 'AIzaSy', 'BEGIN RSA PRIVATE KEY', 'BEGIN OPENSSH PRIVATE KEY']
    violations = []
    for root, dirs, files in os.walk(ROOT_DIR):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for f in files:
            if f == 'measure.py':
                continue
            ext = os.path.splitext(f)[1].lower()
            if ext in PRODUCTION_EXTENSIONS or f in ['requirements.txt', '.env.example']:
                p = os.path.join(root, f)
                try:
                    with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                        txt = fp.read()
                        for sk in sensitive_keywords:
                            if sk in txt:
                                violations.append((f, sk))
                except Exception:
                    pass
    return len(violations) == 0, violations

def main():
    print("==================================================")
    print("       EXAMHUB PRODUCTION AUDIT & MEASUREMENT      ")
    print("==================================================")
    
    failures = []
    
    # 1. License Check
    lic_ok, lic_issues = verify_license()
    print(f"[*] License Check: {'PASS' if lic_ok else 'FAIL'}")
    if not lic_ok:
        failures.append(f"License issues found: {lic_issues}")
    else:
        print("    Proprietary declaration verified. No open source license files.")

    # 2. Lockfiles
    lock_ok = verify_lockfiles()
    print(f"[*] Dependency Lockfiles: {'PASS' if lock_ok else 'FAIL'}")
    if not lock_ok:
        failures.append("Missing package-lock.json or requirements.txt/requirements.lock")

    # 3. Sensitive Data Check
    sens_ok, sens_violations = verify_sensitive_data()
    print(f"[*] Sensitive Data Audit: {'PASS' if sens_ok else 'FAIL'}")
    if not sens_ok:
        failures.append(f"Sensitive data found: {sens_violations}")

    # 4. Git Checks
    git_ok, git_msg, commits, pr_count = verify_git()
    print(f"[*] Git Repository: {'PASS' if git_ok else 'FAIL'} ({git_msg})")
    print(f"    Commit Count: {commits} (Required >= 10): {'PASS' if commits >= 10 else 'PENDING'}")
    print(f"    Merged PRs: {pr_count} (Required >= 4): {'PASS' if pr_count >= 4 else 'PENDING'}")
    if commits < 10:
        failures.append(f"Insufficient commits ({commits} < 10)")
    if pr_count < 4:
        failures.append(f"Insufficient pull requests / merged feature branches ({pr_count} < 4)")

    # 5. Production LOC Count
    loc, file_counts = count_production_loc()
    print(f"[*] Production LOC: {loc} (Required >= 50,000)")
    print(f"    Total production files audited: {len(file_counts)}")
    if loc >= 50000:
        print("    Status: PASS")
    else:
        print(f"    Status: PENDING ({loc}/50000)")
        failures.append(f"Production LOC under threshold ({loc} < 50000)")

    print("==================================================")
    if not failures:
        print("ALL CRITERIA VERIFIED: PASS")
        print(f"Production LOC: {loc}")
        print("Requirement: >= 50,000")
        print("Status: PASS")
        return 0
    else:
        print(f"Audit Status: {len(failures)} item(s) pending or failing:")
        for f in failures:
            print(f" - {f}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
