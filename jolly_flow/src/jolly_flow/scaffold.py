import os
import shutil
import subprocess
from pathlib import Path
from jinja2 import Template

def create_project(name: str, vault_root: str, projects_root: str, templates_dir: str):
    project_slug = name.lower().replace(' ', '-')
    vault_path = Path(vault_root) / project_slug
    repo_path = Path(projects_root) / project_slug

    if vault_path.exists() or repo_path.exists():
        print(f'❌ Error: Project {project_slug} already exists.')
        return

    print(f'🚀 Creating project: {name}')

    # 1. Create Directories
    vault_path.mkdir(parents=True, exist_ok=True)
    repo_path.mkdir(parents=True, exist_ok=True)

    # 2. Init Git
    try:
        subprocess.run(['git', 'init'], cwd=vault_path, check=True, capture_output=True)
        subprocess.run(['git', 'init'], cwd=repo_path, check=True, capture_output=True)
    except Exception as e:
        print(f'⚠️ Git init failed: {e}')

    # 3. Copy & Render Templates
    templates = ['AI-CONTEXT.md.template', 'PROJECT-OVERVIEW.md.template']
    
    for t_name in templates:
        t_path = Path(templates_dir) / t_name
        if not t_path.exists():
            continue

        with open(t_path, 'r') as f:
            template_content = f.read()

        template = Template(template_content)
        rendered = template.render(
            PROJECT_NAME=name,
            PROJECT_SLUG=project_slug,
            CREATED_DATE='2026-01-24',
            MODIFIED_DATE='2026-01-24',
            PROJECT_STATUS='Active',
            CURRENT_PHASE='Phase 0',
            VAULT_PATH=str(vault_path),
            REPO_PATH=str(repo_path)
        )

        dest_name = t_name.replace('.template', '')
        with open(vault_path / dest_name, 'w') as f:
            f.write(rendered)

    # 4. Create .jolly-sync.yaml
    sync_config = f"""vault_root: "{vault_path}"
repo_root: "{repo_path}"
sync:
  - source: "PROJECT-OVERVIEW.md"
    dest: "README.md"
"""
    with open(vault_path / '.jolly-sync.yaml', 'w') as f:
        f.write(sync_config)

    print(f'  ✅ Vault created at: {vault_path}')
    print(f'  ✅ Repo created at: {repo_path}')
    print(f'  ✅ Initial docs rendered.')
