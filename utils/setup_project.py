import os
from pathlib import Path

def create_project_structure(project_name: str = "kingcon_python"):
    """Creates an industry-standard Python project structure."""
    
    # Define the directory structure
    directories = [
        f"src/{project_name}",
        "tests",
        ".github/workflows"
    ]
    
    # Create directories
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {directory}")

    # Create empty __init__.py files to make them proper packages
    Path(f"src/{project_name}/__init__.py").touch()
    Path("tests/__init__.py").touch()
    
    # Define the content for pyproject.toml
    pyproject_content = f"""[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "{project_name}"
version = "0.1.0"
description = "A modern Python project"
readme = "README.md"
requires-python = ">=3.9"
dependencies = []

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "ruff>=0.1.0",
    "mypy>=1.5.0",
]

[project.scripts]
kingcon = "{project_name}.cli:main"

[tool.ruff]
line-length = 88
target-version = "py39"

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
"""

    # Define the content for .gitignore
    gitignore_content = """# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Testing
.pytest_cache/
.coverage
htmlcov/

# IDEs
.vscode/
.idea/
*.swp
"""

    # Write the files
    files = {
        "pyproject.toml": pyproject_content,
        ".gitignore": gitignore_content,
        "README.md": f"# {project_name}\n\nAdd your project description here.",
        f"tests/test_{project_name}.py": f"def test_initial():\n    assert True\n"
    }

    for filename, content in files.items():
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Created file: {filename}")

if __name__ == "__main__":
    # You can change "kingcon_python" to whatever you want your module to be named
    create_project_structure("kingcon_python")
    print("\nProject structure created successfully!")
