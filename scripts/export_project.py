"""
Export Project Code Context

Exports all .py, .json, and .md files from the project into a single file
for easy sharing and context provision.
"""

import os
from pathlib import Path

# Directories to exclude
EXCLUDE_DIRS = {'.venv', 'venv', '.git', '__pycache__', 'node_modules', '.mypy_cache', '.pytest_cache', 'outputs'}

# File extensions to include
INCLUDE_EXTENSIONS = {'.py', '.json', '.md'}

def should_exclude_dir(dir_name):
    """Check if directory should be excluded."""
    return dir_name in EXCLUDE_DIRS or dir_name.startswith('.')

def export_project(root_dir, output_file):
    """
    Export all relevant files to a single context file.
    
    Args:
        root_dir: Root directory to scan
        output_file: Output file path
    """
    root_path = Path(root_dir)
    files_found = []
    
    # Walk through all directories
    for dirpath, dirnames, filenames in os.walk(root_path):
        # Remove excluded directories from the walk
        dirnames[:] = [d for d in dirnames if not should_exclude_dir(d)]
        
        # Process files
        for filename in filenames:
            file_path = Path(dirpath) / filename
            
            # Check if file extension is included
            if file_path.suffix in INCLUDE_EXTENSIONS:
                files_found.append(file_path)
    
    # Sort files for consistency
    files_found.sort()
    
    # Write to output file
    with open(output_file, 'w', encoding='utf-8') as out_f:
        out_f.write(f"PROJECT CODE CONTEXT EXPORT\n")
        out_f.write(f"Total files: {len(files_found)}\n")
        out_f.write(f"{'='*80}\n\n")
        
        for file_path in files_found:
            # Get relative path
            rel_path = file_path.relative_to(root_path)
            
            # Write separator and filename
            out_f.write(f"\n{'='*80}\n")
            out_f.write(f"FILE: {rel_path}\n")
            out_f.write(f"{'='*80}\n\n")
            
            # Write file content
            try:
                with open(file_path, 'r', encoding='utf-8') as in_f:
                    content = in_f.read()
                    out_f.write(content)
                    out_f.write('\n\n')
            except Exception as e:
                out_f.write(f"[ERROR reading file: {e}]\n\n")
    
    return len(files_found)

if __name__ == "__main__":
    # Get current directory
    project_dir = Path(__file__).parent
    output_path = project_dir / "FULL_CODE_CONTEXT.txt"
    
    print(f"Exporting project from: {project_dir}")
    print(f"Output file: {output_path}")
    print(f"\nScanning...")
    
    num_files = export_project(project_dir, output_path)
    
    print(f"\n✅ Export complete!")
    print(f"   Files exported: {num_files}")
    print(f"   Output: {output_path}")
    
    # Show file size
    file_size = output_path.stat().st_size
    if file_size > 1024 * 1024:
        size_str = f"{file_size / (1024*1024):.2f} MB"
    elif file_size > 1024:
        size_str = f"{file_size / 1024:.2f} KB"
    else:
        size_str = f"{file_size} bytes"
    
    print(f"   Size: {size_str}")
