#!/usr/bin/env python3
"""
Validates that every skill in the skills/ directory complies with the Agent Skills standard (agentskills.io):
1. Must be inside its own directory under skills/<skill-name>/
2. Must contain SKILL.md
3. SKILL.md must start with YAML frontmatter bounded by '---'
4. Frontmatter must contain 'name' matching the directory name
5. Frontmatter must contain a descriptive 'description'
"""

import os
import sys

def main():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    skills_dir = os.path.join(repo_root, "skills")
    
    if not os.path.exists(skills_dir):
        print(f"Error: skills directory not found at {skills_dir}")
        sys.exit(1)
        
    failures = []
    passed = 0
    
    skill_folders = sorted(os.listdir(skills_dir))
    for folder in skill_folders:
        folder_path = os.path.join(skills_dir, folder)
        if not os.path.isdir(folder_path):
            continue
            
        skill_file = os.path.join(folder_path, "SKILL.md")
        if not os.path.exists(skill_file):
            failures.append(f"{folder}: Missing SKILL.md")
            continue
            
        try:
            with open(skill_file, "r", encoding="utf-8") as f:
                content = f.read()
                
            if not content.startswith("---"):
                failures.append(f"{folder}: SKILL.md does not start with YAML frontmatter '---'")
                continue
                
            parts = content.split("---", 2)
            if len(parts) < 3:
                failures.append(f"{folder}: Malformed YAML frontmatter (missing closing '---')")
                continue
                
            front = parts[1]
            name_line = None
            desc_line = None
            
            for line in front.splitlines():
                stripped = line.strip()
                if stripped.startswith("name:"):
                    name_line = stripped
                elif stripped.startswith("description:"):
                    desc_line = stripped
                    
            if not name_line:
                failures.append(f"{folder}: Missing 'name' in YAML frontmatter")
                continue
            if not desc_line:
                failures.append(f"{folder}: Missing 'description' in YAML frontmatter")
                continue
                
            skill_name = name_line.split("name:", 1)[1].strip().strip('"').strip("'")
            if skill_name != folder:
                failures.append(f"{folder}: Name in frontmatter ('{skill_name}') does not match directory name ('{folder}')")
                continue
                
            passed += 1
        except Exception as e:
            failures.append(f"{folder}: Error reading file - {str(e)}")
            
    print(f"=== Validation Report ===")
    print(f"Total skills checked: {len(skill_folders)}")
    print(f"Passed: {passed}")
    print(f"Failed: {len(failures)}")
    
    if failures:
        print("\nFailures:")
        for fail in failures:
            print(f"  - {fail}")
        sys.exit(1)
        
    print("\nAll skills comply with the Agent Skills standard! ✨")

if __name__ == "__main__":
    main()
