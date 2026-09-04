"""
ExamHub Zip Archive Builder
Packages the complete ExamHub codebase including the .git repository,
excluding temporary caches, node_modules, and build directories.
"""

import os
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TARGET_ZIP_LOCAL = ROOT / "examhub.zip"
TARGET_ZIP_DESKTOP = ROOT.parent / "examhub.zip"

EXCLUDE_DIRS = {
    "node_modules", "dist", "build", ".pytest_cache", "__pycache__",
    "coverage", "htmlcov", ".venv", "venv", ".idea", ".vscode"
}

EXCLUDE_FILES = {
    "examhub.zip", "create_examhub_zip.py", "verify_teacher_update_student_sync.py"
}

def make_zip(dest_path: Path):
    print(f"Creating archive at {dest_path}...")
    file_count = 0
    git_file_count = 0

    with zipfile.ZipFile(dest_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(ROOT):
            rel_root = os.path.relpath(root, ROOT)
            
            # Filter excluded dirs (but KEEP .git!)
            dirs[:] = [
                d for d in dirs
                if d not in EXCLUDE_DIRS and not d.endswith(".egg-info")
            ]

            for f in files:
                if f in EXCLUDE_FILES or f.endswith(".pyc") or f.endswith(".pyo") or f.endswith(".sqlite3"):
                    continue

                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, ROOT)

                # Skip if inside an excluded directory
                parts = Path(rel_path).parts
                if any(p in EXCLUDE_DIRS for p in parts):
                    continue

                zf.write(full_path, arcname=rel_path)
                file_count += 1
                if ".git" in parts:
                    git_file_count += 1

    size_mb = dest_path.stat().st_size / (1024 * 1024)
    print(f"Archived {file_count} files ({git_file_count} in .git). Size: {size_mb:.2f} MB")

def main():
    make_zip(TARGET_ZIP_LOCAL)
    try:
        make_zip(TARGET_ZIP_DESKTOP)
    except Exception as e:
        print(f"Notice: Could not write to desktop: {e}")

if __name__ == "__main__":
    main()
